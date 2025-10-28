"""
context_manager.py
-------------------
Takes the transcript (list of dicts) and breaks it into text chunks.
Used before sending text to Gemini for summarization or Q&A.
"""

import json

def build_context(transcript_data, max_chars=150):
    """
    Creates chunks of transcript text for processing (Gemini context).

    Args:
        transcript_data (list): List of transcript segments — can be either:
            - list[dict]: each dict has 'text' key (and possibly timestamps)
            - list[str]: plain transcript lines
        max_chars (int): Maximum number of characters per chunk.

    Returns:
        list[str]: List of chunk strings, each <= max_chars.
    """
    chunks = []
    current_chunk = ""

    for segment in transcript_data:
        if isinstance(segment, dict):
            text = str(segment.get("text", "")).strip()
        elif isinstance(segment, str):
            text = segment.strip()
        else:
            text = str(segment).strip()

        if not text:
            continue 

        if len(current_chunk) + len(text) + 1 <= max_chars:
            current_chunk += " " + text if current_chunk else text
        else:
            chunks.append(current_chunk.strip())
            current_chunk = text

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    with open("transcript.json", "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    chunks = build_context(transcript_data)
    print(f"✅ Created {len(chunks)} chunks.")

    with open("context.json", "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks}, f, indent=4)
