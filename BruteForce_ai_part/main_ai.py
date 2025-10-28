from modules.gemini_pipeline import process_watched_transcript

def main(transcript_chunks, user_question):
    """
    Main AI logic — receives transcript chunks already limited to watched part,
    and returns AI-generated answer, summary, and key points.
    """
    if not transcript_chunks:
        return {"error": "No transcript data received."}

    # Combine chunks into a single text context
    context_text = "\n\n".join([chunk['text'] for chunk in transcript_chunks])

    # Send context + question to Gemini
    result = process_watched_transcript(
        context_text,
        user_question=user_question,
        tts=False  # set True if text-to-speech output is required
    )

    return result
