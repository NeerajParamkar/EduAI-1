import pyttsx3
import os

def text_to_speech(text, output_path="output_audio.mp3"):
    """
    Converts given text to speech and saves it as an audio file.

    Parameters:
        text (str): Text to convert to speech.
        output_path (str): Path to save the audio file.

    Returns:
        str: Path of the saved audio file.
    """
    # Initialize TTS engine
    engine = pyttsx3.init()

    # Optional: set properties (voice, rate, volume)
    engine.setProperty('rate', 150)      # Speed of speech
    engine.setProperty('volume', 1.0)    # Volume (0.0 to 1.0)

    # Save to file
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    return os.path.abspath(output_path)
