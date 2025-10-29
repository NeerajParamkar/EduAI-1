from modules.tts_engine import speak_text  # ✅ Correct path

def getairesponce(ans: str):
    """Speak the AI response."""
    try:
        speak_text(ans, voice="nPczCjzI2devNBz1zQrb")
    except Exception as e:
        print(f"[ERROR] Failed to speak text: {e}")
