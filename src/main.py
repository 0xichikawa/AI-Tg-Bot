import nest_asyncio
import platform
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Voice
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    PicklePersistence,
    MessageHandler,
    CommandHandler,
)
import asyncio
import telegram.ext.filters as filters
from aiAnswer import generateAnswer
import os
import dotenv

import requests
import json

dotenv.load_dotenv(override=True)

TOKEN_TELEGRAM = os.getenv("TG_TOKEN")
print(f"bot token is @{TOKEN_TELEGRAM}")
# Constants
helpText = f"""
This is a simple telegram bot.

<b>Commands:</b>\n

🔍 /ask: Get instant answers to your equipment and project questions.\n
🎬 /voice: Get voice responses to your queries with clear audio.\n
📝 /help: Unsure what to do? Use the /help command to see a list of available commands.\n

<b>How to Use:</b>\n

<b>For Equipment Recommendations:</b> Simply use /ask followed by your query\n
e.g., /ask what's your name?\n
<b>For Voice Queries:</b> Activate voice responses with /voice followed by your question\n
e.g., /voice what's your role?\n
<b>For General Assistance:</b> Need guidance? Type /help to see how I can assist you further.\n

"""
homepageBtn = InlineKeyboardButton(
    text="🌎Website", url="https://telegram-miniapp-three.vercel.app/"
)
docsBtn = InlineKeyboardButton(text="📜Help", callback_data="docs Btn")
keyboard_markup = InlineKeyboardMarkup(
    [
        [homepageBtn, docsBtn],  # This is a row with two buttons
    ]
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def get_gpt4_response(prompt):
    answer = generateAnswer(prompt)
    return f"{answer}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userName = update.message.chat.username
    userId = str(update.message.chat.id)
    storage_file_path = "thread_storage.json"
    # Initialize an empty dictionary to store threadIds
    thread_ids = {}
    # Check if the storage file exists and read the threadIds if it does
    if os.path.exists(storage_file_path):
        with open(storage_file_path, "r") as file:
            thread_ids = json.load(file)
    else:
        with open(storage_file_path, "w") as file:
            json.dump(thread_ids, file)
    all_keys = list(thread_ids.keys())
    # Check if the specific user_id exists in the dictionary
    if userId in all_keys:
        pass
    else:
        thread_ids[userId] = userName
        # Save the updated dictionary to the storage file
        with open(storage_file_path, "w") as file:
            json.dump(thread_ids, file)
    answer = f"""
🚀 <b>Welcome to @{userName} !</b>\n
{helpText}
"""

    response_text = f"{answer}\n"
    await update.message.reply_html(response_text, reply_markup=keyboard_markup)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.removeprefix("/ask").strip()

    if user_message != "":
        thinking_message = await update.message.reply_text("🤖 typing...")
        # Await the response from GPT-4
        answer = await get_gpt4_response(user_message)
        response_text = f"{answer}\n\n"
        await thinking_message.edit_text(
            text=response_text, reply_markup=keyboard_markup, parse_mode=ParseMode.HTML
        )
    else:
        answer = """
<b>🪫 Prompt is empty. Please provide a prompt.</b>\n
for example: <code>/ask What's your name?</code>
"""
        response_text = f"{answer}\n\n"

        await update.message.reply_html(response_text, reply_markup=keyboard_markup)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = helpText
    response_text = f"{answer}\n"
    await update.message.reply_html(response_text, reply_markup=keyboard_markup)


async def helpBtn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the button click."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button click
    # Extract the callback data from the clicked button
    callback_data = query.data
    answer = helpText
    response_text = f"{answer}\n"
    await query.message.reply_html(response_text, reply_markup=keyboard_markup)

def main() -> None:
    """Run the bot."""
    # Apply nest_asyncio to handle nested event loops
    nest_asyncio.apply()
    
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    application = (
        Application.builder()
        .token(TOKEN_TELEGRAM)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    # Add your handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", ask))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CallbackQueryHandler(helpBtn))

    # Platform-specific event loop setup
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
