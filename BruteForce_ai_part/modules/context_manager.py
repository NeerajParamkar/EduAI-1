# modules/context_manager.py

def get_transcript_chunks(transcript_segments, watched_time, chunk_size=50):
    """
    General function to get transcript chunks from any transcript data.

    transcript_segments: list of dicts with 'text', 'starttime', 'endtime'
    watched_time: float, seconds of video watched
    chunk_size: int, number of words per chunk

    Returns:
        list of text chunks up to watched_time
    """
    # Filter segments within watched time
    watched_segments = [seg['text'] for seg in transcript_segments
                        if seg['starttime'] <= watched_time]

    if not watched_segments:
        return []

    # Combine all text
    full_text = " ".join(watched_segments)

    # Split into chunks of chunk_size words
    words = full_text.split()
    chunks = [" ".join(words[i:i+chunk_size])
              for i in range(0, len(words), chunk_size)]
    return chunks
