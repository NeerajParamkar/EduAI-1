# import json
# from modules.context_manager import build_context
# from modules.gemini_pipeline import process_watched_transcript
# from modules.tts_handler import getairesponce

# def main(transcript_data, user_question=None):
#     """
#     Orchestrates the full pipeline using in-memory transcript JSON.

#     Args:
#         transcript_data (list[dict]): Transcript data (list of dicts containing text, starttime, endtime)
#         user_question (str): User's question to ask Gemini.

#     Returns:
#         dict: Final structured output from Gemini.
#     """
#     print("[INFO] Using provided transcript JSON...")
    
#     if not isinstance(transcript_data, list):
#         raise ValueError("Transcript data must be a list of dictionaries.")
#     for i, item in enumerate(transcript_data):
#         if not all(k in item for k in ("text", "starttime", "endtime")):
#             raise ValueError(f"Missing required keys in transcript at index {i}: {item}")

#     print("[INFO] Chunking transcript into sections...")
#     chunks = build_context(transcript_data)

#     print("[INFO] Sending to Gemini model...")
#     result = process_watched_transcript(chunks, user_question=user_question)

#     print("\n✅ Gemini Response:")
#     print(json.dumps(result, indent=4, ensure_ascii=False))
#     getairesponce(result)
#     return result

import json
from modules.context_manager import build_context
from modules.gemini_pipeline import process_watched_transcript
from modules.tts_handler import getairesponce

def main(transcript_data, user_question=None):
    """
    Orchestrates the full pipeline using in-memory transcript JSON.

    Args:
        transcript_data (list[dict]): Transcript data (list of dicts containing text, starttime, endtime)
        user_question (str): User's question to ask Gemini.

    Returns:
        dict: Final structured output from Gemini.
    """
    print("[INFO] Using provided transcript JSON...")

    # Validate transcript data
    if not isinstance(transcript_data, list):
        raise ValueError("Transcript data must be a list of dictionaries.")
    for i, item in enumerate(transcript_data):
        if not all(k in item for k in ("text", "starttime", "endtime")):
            raise ValueError(f"Missing required keys in transcript at index {i}: {item}")

    print("[INFO] Chunking transcript into sections...")
    chunks = build_context(transcript_data)

    print("[INFO] Sending to Gemini model...")
    result = process_watched_transcript(chunks, user_question=user_question)

    print("\n✅ Gemini Response:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # Extract the actual AI text to speak
    ai_text = None
    if isinstance(result, dict):
        # Common keys that may contain AI response text
        ai_text = result.get("answer") or result.get("response") or result.get("text") or None
    elif isinstance(result, str):
        ai_text = result

    # if ai_text:
        # getairesponce(ai_text)
    #     # print(ai_text)
    # else:
    #     print("[WARN] No suitable AI response text found for TTS.")

    return result
