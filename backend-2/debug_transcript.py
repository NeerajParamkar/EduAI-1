import sys
import os

# Add the parent directory to sys.path so Python can find the modules
sys.path.append(r'D:\bfeduai\backend-2')

from app.db.database import transcripts_collection
from app.api.routes_transcript import getytscript, insertdb, get_youtube_id

def test_transcript_storage():
    # Clear the database first for a clean test
    transcripts_collection.delete_many({})
    print("Database cleared")
    
    # Test with a real YouTube video ID that has transcripts
    # Using a video that's known to have transcripts
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # YouTube's first video
    video_id = get_youtube_id(test_url)
    
    print(f"Video ID: {video_id}")
    
    if video_id:
        try:
            # Get the transcript
            print("Fetching transcript...")
            transcript = getytscript(video_id)
            print(f"Transcript fetched: {type(transcript)}")
            print(f"Transcript length: {len(transcript) if isinstance(transcript, str) else 'Not a string'}")
            
            # Try to insert into database
            print("Inserting into database...")
            result = insertdb(video_id, test_url, transcript)
            print(f"Insert result: {result}")
            
            # Check if it was actually stored
            stored_record = transcripts_collection.find_one({"video_id": video_id})
            if stored_record:
                print("Transcript successfully stored in database!")
                print(f"Stored record keys: {list(stored_record.keys())}")
                print(f"Transcript type in DB: {type(stored_record.get('transcript', 'Not found'))}")
            else:
                print("Transcript was not stored in database!")
                
        except Exception as e:
            print(f"Error occurred: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Could not extract video ID from URL")

if __name__ == "__main__":
    test_transcript_storage()