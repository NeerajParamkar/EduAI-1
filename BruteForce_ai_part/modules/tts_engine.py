import io
import pygame
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

load_dotenv()
TTS_API_KEY = os.getenv("TTS_API_KEY")
if not TTS_API_KEY:
    raise ValueError("❌ TTS_API_KEY not found in environment")

client = ElevenLabs(api_key=TTS_API_KEY)

def speak_text(text: str, voice: str):
    if not text.strip():
        raise ValueError("No text provided for TTS.")

    print("[INFO] Generating speech via ElevenLabs...")

    audio_gen = client.text_to_speech.convert(
        voice_id=voice,
        model_id="eleven_multilingual_v1",
        text=text
    )
    audio_bytes = b"".join(audio_gen)

    # Save to a temporary MP3 in memory
    temp_file = "temp_tts.mp3"
    with open(temp_file, "wb") as f:
        f.write(audio_bytes)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
