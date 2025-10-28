"""
main_ai.py
-----------
Central pipeline controller for transcript-based Q&A using Gemini API.

Flow:
1. Read transcript JSON (from file or API) → read_transcript_module.py
2. Chunk transcript text intelligently → context_manager.py
3. Send context + user question to Gemini → gemini_pipeline.py
4. Return final structured JSON { "answer": "...", "key_points": [...] }
"""

import json
from read_transcript_module import load_transcript_from_txt
from modules.context_manager import build_context
from modules.gemini_pipeline import process_watched_transcript


def main(transcript_path, user_question=None):
    """
    Orchestrates the full pipeline.

    Args:
        transcript_path (str): Path to JSON transcript file.
        user_question (str): User's question to ask Gemini.

    Returns:
        dict: Final structured output from Gemini.
    """

    print("[INFO] Reading transcript...")
    transcript_data = load_transcript_from_txt(transcript_path)

    print("[INFO] Chunking transcript into sections...")
    chunks = build_context(transcript_data)

    print("[INFO] Sending to Gemini model...")
    result = process_watched_transcript(chunks, user_question=user_question)

    print("\n✅ Gemini Response:")
    print(json.dumps(result, indent=4,ensure_ascii=False))

    return result


if __name__ == "__main__":
    transcript_path = "EduAI-1/BruteForce_ai_part/transcript.txt"
    question = "What is the video about? Can you explain in kannada?"

    output = main(transcript_path, user_question=question)
