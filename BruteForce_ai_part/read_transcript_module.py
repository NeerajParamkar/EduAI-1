import json

def load_transcript(transcript_input):
    """
    Loads transcript data from a JSON string or Python list and returns
    it as a validated list of dictionaries.

    The transcript is assumed to already contain only the watched portion of the video.

    Args:
        transcript_input (str | list): Either:
            - A JSON string (e.g., from API or frontend)
            - A Python list of dicts (already parsed)

    Returns:
        list[dict]: Transcript data with validated 'text', 'starttime', and 'endtime' fields.
    """

    # --- Handle JSON string input ---
    if isinstance(transcript_input, str):
        data = transcript_input.strip()
        if data.startswith("{"):
            data = "[" + data + "]"

        try:
            transcript = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON structure in transcript: {e}")

    # --- Handle already parsed list ---
    elif isinstance(transcript_input, list):
        transcript = transcript_input

    else:
        raise TypeError("Transcript input must be a JSON string or a Python list.")

    # --- Validate structure ---
    for i, item in enumerate(transcript):
        if not isinstance(item, dict):
            raise ValueError(f"Invalid entry at index {i}: must be a dict")
        if not all(k in item for k in ("text", "starttime", "endtime")):
            raise ValueError(f"Missing required keys at index {i}: {item}")

    return transcript