import json
from modules.gemini_pipeline import process_watched_transcript

def load_transcript_from_txt(file_path):
    """Reads transcript JSON-like data from a text file and returns as a list."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
        # Convert the text to a valid JSON list if necessary
        if data.strip().startswith("{"):
            data = "[" + data + "]"
        transcript = json.loads(data)
    return transcript

def summarize_watched_portion(transcript, watched_until):
    """Filters transcript up to a certain time and gets summary."""
    watched_part = [t for t in transcript if t["endtime"] <= watched_until]
    return process_watched_transcript(watched_part)
