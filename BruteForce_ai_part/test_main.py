from read_transcript_module import load_transcript_from_txt, summarize_watched_portion

transcript = load_transcript_from_txt("transcript.txt")
watched_until = 15  # seconds watched

result = summarize_watched_portion(transcript, watched_until)
print("\n--- Gemini Output ---\n")
print(result)
