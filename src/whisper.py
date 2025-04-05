import openai
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client = openai.Client(api_key = OPENAI_API_KEY)
def generateAudio(voiceOver):
    speech_file_path = "audio.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=f"{voiceOver}"
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path
def generateTranscribe(filePath):
    audio_file= open(f"{filePath}", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)
    return transcription.text