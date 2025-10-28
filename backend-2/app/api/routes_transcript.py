from fastapi import APIRouter, Depends, HTTPException
from app.db.database import transcripts_collection
database_collection = transcripts_collection
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import json
from urllib.parse import urlparse, parse_qs
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/transcript", tags=["Transcript"])

class VideoRequest(BaseModel):
    video_id: str

class UrlData(BaseModel):
    url: str

class TranscriptTimeRange(BaseModel):
    video_id: str
    start_time: float
    end_time: float

def get_youtube_id(url):
    """
    Extracts the YouTube video ID from a URL.
    Works for both long and short YouTube links.
    """
    parsed_url = urlparse(url)
    
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query).get('v', [None])[0]
    
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path.lstrip('/')
    
    else:
        return None

def getytscript(video_id):
    ytt_api = YouTubeTranscriptApi()
    try:
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
    except NoTranscriptFound:
        print("English transcript not found. Trying auto-generated Hindi...")
        try:
            fetched_transcript = ytt_api.fetch(video_id, languages=['hi'])
        except NoTranscriptFound:
            print("No transcripts available for this video")
            exit()

    # Convert to your custom format
    transcript_json = []
    for snippet in fetched_transcript:
        entry = {
            "text": snippet.text,                           # Use dot notation
            "starttime": snippet.start,                     # Use dot notation
            "endtime": snippet.start + snippet.duration     # Use dot notation
        }
        transcript_json.append(entry)

    yt_transcript=(json.dumps(transcript_json, indent=4, ensure_ascii=False))
    # print(yt_transcript)
    return yt_transcript

def insertdb(video_id, url, transcript_json):
    existing = database_collection.find_one({"url": url})
    
    if existing:
        print(f"⚠️ Transcript for video_id '{video_id}' already exists. Skipping insert.")
        return False  # Optional: return False if not inserted

    # Insert if not present
    data = {
        "video_id": video_id,
        "url": url,
        "transcript": transcript_json
    }
    database_collection.insert_one(data)
    print("✅ Transcript saved to MongoDB successfully!")
    return True  # Optional: return True if inserted

@router.post("/get-transcript")
def get_transcript(data: VideoRequest):
    
    video_id = data.video_id

    # Fetch from MongoDB
    record = database_collection.find_one({"video_id": video_id}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="Transcript not found in database")

    # Handle older JSON string format
    transcript = record.get("transcript", [])
    if isinstance(transcript, str):
        transcript = json.loads(transcript)

    record["transcript"] = transcript
    return JSONResponse(content=record)

@router.post("/get-transcript-by-time")
def get_transcript_by_time(data: TranscriptTimeRange):
    """
    POST /get-transcript-by-time
    {
        "video_id": "Ckc0gS9Kvrg",
        "start_time": 30,
        "end_time": 60
    }
    """
    # Fetch record from MongoDB
    record = database_collection.find_one({"video_id": data.video_id}, {"_id": 0})
    if not record:
        raise HTTPException(status_code=404, detail="Transcript not found")

    transcript = record.get("transcript", [])

    # Convert if stored as string
    if isinstance(transcript, str):
        transcript = json.loads(transcript)

    # 🔍 Find entries that fall within the range
    filtered_transcript = [
        entry for entry in transcript
        if entry["endtime"] >= data.start_time and entry["starttime"] <= data.end_time
    ]

    if not filtered_transcript:
        return JSONResponse(content={"message": "No transcript found for given range."}, status_code=404)

    return {
        "video_id": data.video_id,
        "requested_start_time": data.start_time,
        "requested_end_time": data.end_time,
        "filtered_transcript": filtered_transcript,
        "total_entries": len(filtered_transcript)
    }
@router.post("/process_url")
def process_url(data: UrlData):
    received_url = data.url
    # print("URL from frontend:", received_url)
    ytid=get_youtube_id(received_url)
    print(ytid)
    tc=getytscript(ytid)
    insertdb(ytid,received_url,tc)
    # print(tc)
    # get_transcript_by_time_range(ytid,0,30)
    return {"message": f"URL received successfully: {received_url}"}
