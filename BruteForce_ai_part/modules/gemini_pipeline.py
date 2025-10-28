# modules/gemini_pipeline.py

from modules.gemini_handler import ask_gemini
from modules.tts_engine import text_to_speech

def process_watched_transcript(context_text, user_question=None, video_id=None, tts=True):
    """
    Handles question answering, summarization, and key points extraction in one wrapper.

    context_text: str - transcript text up to watched portion
    user_question: str - optional user question
    video_id: str - used for saving TTS audio
    tts: bool - whether to generate audio for the answer
    """
    result = {}

    # 1️⃣ Answer user question
    if user_question:
        result['answer'] = ask_gemini(user_question, context_text)
        if tts and video_id:
            audio_file = f"data/audio_responses/{video_id}_answer.mp3"
            text_to_speech(result['answer'], filename=audio_file)
            result['audio_file'] = audio_file

    # 2️⃣ Summary of watched portion
    
    return result
