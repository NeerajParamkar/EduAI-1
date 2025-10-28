# main_ai.py

from modules.context_manager import get_transcript_chunks
from modules.gemini_pipeline import process_watched_transcript

def main():
    video_id = "VIDEO_ID_HERE"

    # 1️⃣ Fetch transcript from DB (replace with your actual DB call)
    # transcript_segments = fetch_transcript_from_db(video_id)
    transcript_segments = fetch_transcript_from_db(video_id)  # should return list of dicts: [{'text':..., 'starttime':..., 'endtime':...}, ...]

    # Get how much of the video the user has watched (in seconds)
    watched_time = 600  # example: 10 minutes watched

    # 3️⃣ User question
    user_question = "Explain the main concept covered so far."

    # 4️⃣ Get transcript chunks up to watched time
    context_chunks = get_transcript_chunks(transcript_segments, watched_time)
    if not context_chunks:
        print("No transcript available for the watched portion.")
        return

    context_text = "\n\n".join(context_chunks)

    # 5️⃣ Process everything with Gemini: answer + summary + key points + optional TTS
    result = process_watched_transcript(
        context_text,
        user_question=user_question,
        video_id=video_id,
        tts=True  # set False if you don't want audio
    )

    # 6️⃣ Print outputs
    print("\n=== Gemini Answer ===\n")
    print(result.get('answer', 'No answer returned'))

    print("\n=== Summary ===\n")
    print(result.get('summary', 'No summary returned'))

    print("\n=== Key Points ===\n")
    print(result.get('key_points', 'No key points returned'))

    if 'audio_file' in result:
        print(f"\nAudio saved at: {result['audio_file']}")

if __name__ == "__main__":
    main()
