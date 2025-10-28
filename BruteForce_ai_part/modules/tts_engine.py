import pyttsx3

def text_to_speech(text, filename="output_audio.mp3"):
    """Converts text to speech and saves it as an audio file."""
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename
