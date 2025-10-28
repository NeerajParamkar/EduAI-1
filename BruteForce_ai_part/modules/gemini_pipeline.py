"""
gemini_pipeline.py
-------------------
Complete pipeline:
- Takes raw transcript (list of dicts)
- Builds readable chunks using context_manager
- Sends to Gemini via gemini_handler
- Returns structured JSON (answer + key_points)
"""

import json
from modules.context_manager import build_context
from modules.gemini_handler import ask_gemini


def process_watched_transcript(transcript_data, user_question=None):
    """
    Processes transcript data + user question through Gemini.
    
    Args:
        transcript_data (list): List of transcript dicts [{text, starttime, endtime}, ...]
        user_question (str): Optional question asked by the user.

    Returns:
        dict: {
            "answer": "..."
            }
    """
    chunks = build_context(transcript_data)
    if not chunks:
        return {"answer": "Sorry please try again later."}

    context_text = "\n\n".join(chunks)
    if not user_question:
        user_question = "Summarize the main concepts covered so far."
    gemini_response = ask_gemini(user_question, context_text)

    try:
        parsed = json.loads(gemini_response)
        if isinstance(parsed, dict):
            result = {
                "answer": parsed.get("answer", "")
            }
        else:
            result = {"answer": gemini_response}
    except json.JSONDecodeError:
        lines = gemini_response.split("\n")
        result = {
            "answer": gemini_response
        }

    return result


if __name__ == "__main__":
    from read_transcript_module import load_transcript_from_txt

    transcript = load_transcript_from_txt("transcript.json")

    question = "Explain the main concepts discussed so far."
    output = process_watched_transcript(transcript, user_question=question)

    print("\n--- Gemini Output ---\n")
    print(json.dumps(output, indent=4))
