import json
import os

def load_transcript_from_txt(file_path: str):
    """
    Reads a JSON or text-based transcript file and returns it as a list of dictionaries.
    The file is assumed to already contain only the watched portion of the video."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Transcript file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read().strip()

    if data.startswith("{"):
        data = "[" + data + "]"

    try:
        transcript = json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON structure in transcript: {e}")

    for i, item in enumerate(transcript):
        if not isinstance(item, dict):
            raise ValueError(f"Invalid entry at index {i}: must be a dict")
        if not all(k in item for k in ("text", "starttime", "endtime")):
            raise ValueError(f"Missing required keys at index {i}: {item}")

    return transcript


def summarize_watched_portion(file_path: str):
    """
    Loads the transcript JSON file (already watched portion)
    and returns it as-is for downstream Gemini processing.
    """
    transcript = load_transcript_from_txt(file_path)
    return transcript

if __name__ == "__main__":
    path = "transcript.json"
    transcript_data = summarize_watched_portion(path)
    print(json.dumps(transcript_data[:3], indent=2))
