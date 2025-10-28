"""
main_ai.py
-----------
Central pipeline controller for transcript-based Q&A using Gemini API
and optional quiz generation.
"""

import json
import os
from read_transcript_module import load_transcript_from_txt
from modules.context_manager import build_context
from modules.gemini_pipeline import process_watched_transcript
from modules.quiz_mode import run_quiz  # Quiz integration


def main(transcript_path, user_question=None, quiz_mode=False, num_quiz_questions=5):
    """
    Orchestrates the AI pipeline for chatbot or quiz mode.

    Args:
        transcript_path (str): Path to transcript JSON/txt file (watched portion).
        user_question (str): User's question for chatbot mode.
        quiz_mode (bool): If True, runs the interactive quiz.
        num_quiz_questions (int): Number of quiz questions to generate.

    Returns:
        dict or list:
            - Chatbot mode: {"answer": "...", "key_points": [...]}
            - Quiz mode: [{"question": "...", "user_answer": "...", "correct_answer": "..."}]
    """

    # --- Step 1: Validate transcript path ---
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript file not found: {transcript_path}")

    # --- Step 2: Load transcript ---
    transcript_data = load_transcript_from_txt(transcript_path)

    # --- Step 3: Split into chunks for processing ---
    chunks = build_context(transcript_data)

    # --- Step 4: Quiz Mode ---
    if quiz_mode:
        print("\n🎯 Quiz Mode Activated!")
        results = run_quiz(chunks, num_questions=num_quiz_questions)
        print(json.dumps(results, indent=4, ensure_ascii=False))
        return results

    # --- Step 5: Chatbot Mode ---
    if not user_question:
        raise ValueError("Please provide a question when quiz_mode=False.")

    result = process_watched_transcript(chunks, user_question=user_question)

    print("\n✅ Gemini Response:")
    print(json.dumps(result, indent=4, ensure_ascii=False))

    return result


if __name__ == "__main__":
    transcript_path = "EduAI-1/BruteForce_ai_part/transcript.txt"

    # Chatbot example
    question = "What is the video about? Can you explain in Kannada?"
    output = main(transcript_path, user_question=question)

    # Uncomment to test Quiz mode
    # quiz_results = main(transcript_path, quiz_mode=True, num_quiz_questions=3)
    # print(quiz_results)
