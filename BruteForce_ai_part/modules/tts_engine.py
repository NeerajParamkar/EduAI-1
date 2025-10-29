import io
import pygame
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os
import tempfile
import pygame

load_dotenv()
# TTS_API_KEY = os.getenv("")
TTS_API_KEY = ""
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

    # ✅ Use a unique temporary file to avoid locking
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_path = temp_file.name
        temp_file.write(audio_bytes)

    try:
        # Initialize pygame mixer (re-init if already active)
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.mixer.init()

        # Load and play safely
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()

        # Wait until playback finishes
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    finally:
        # ✅ Always clean up the file after playback
        try:
            os.remove(temp_path)
        except Exception as e:
            print(f"[WARN] Could not delete temp file: {e}")
