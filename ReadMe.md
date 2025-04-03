# Kokoa Bot 🤖

A powerful Telegram bot that combines voice interactions, text responses, and GPT-4 capabilities to provide an engaging user experience.

## Features ✨

- **Smart Conversations**: Powered by GPT-4 for intelligent responses
- **Voice Interaction**: Support for voice messages and text-to-speech
- **Audio Transcription**: Convert voice messages to text using Whisper AI
- **Interactive UI**: Clean interface with inline buttons

## Commands 🎯

- `/start` - Initialize the bot and get welcome message
- `/ask` - Get text responses to your questions
- `/voice` - Receive voice responses to your queries
- `/help` - View all available commands and usage instructions

## Setup 🛠️

1. Install required packages:
```bash
pip install python-telegram-bot openai python-dotenv
```

2. Create a `.env` file with your API keys:
```
TG_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_api_key
```

3. Run the bot:
```bash
python bot.py
```

## Usage Examples 💡

- Text query: `/ask What's your name?`
- Voice response: `/voice Tell me about yourself`
- Send a voice message to get AI-powered responses

## Tech Stack 🔧

- Python-Telegram-Bot
- OpenAI GPT-4
- Whisper AI for voice transcription
- Text-to-Speech capabilities

## Made with ❤️ by HighTech

[Visit Website](https://telegram-miniapp-three.vercel.app/)
