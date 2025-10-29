# app/api/router_chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from pymongo import MongoClient

# Initialize Router
router = APIRouter(prefix="/auth", tags=["Chat"])

# MongoDB Connection (Replace with your own URI)
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_database"]
collection = db["chat_messages"]

# ---------------------- MODELS ----------------------

class ChatMessage(BaseModel):
    video_id: str
    user_email: str
    message: str

class ChatHistoryResponse(BaseModel):
    video_id: str
    user_email: str
    messages: List[dict]

# ---------------------- ROUTES ----------------------

@router.post("/send_message")
def send_message(data: ChatMessage):
    """Store user message, generate AI reply, and save both in DB."""
    timestamp = datetime.now().isoformat()

    # Save user message
    user_entry = {
        "video_id": data.video_id,
        "user_email": data.user_email,
        "role": "user",
        "text": data.message,
        "timestamp": timestamp
    }
    collection.insert_one(user_entry)

    # Generate mock AI response (replace later with your AI function)
    ai_text = f"That's an excellent question about '{data.message}'. Here's what I can explain..."
    ai_entry = {
        "video_id": data.video_id,
        "user_email": data.user_email,
        "role": "ai",
        "text": ai_text,
        "timestamp": datetime.now().isoformat()
    }
    collection.insert_one(ai_entry)

    return {
        "status": "success",
        "response": ai_text,
        "timestamp": ai_entry["timestamp"]
    }

@router.get("/get_chat_history", response_model=ChatHistoryResponse)
def get_chat_history(video_id: str, user_email: str):
    """Fetch complete chat history for a specific user and video."""
    chats = list(
        collection.find(
            {"video_id": video_id, "user_email": user_email},
            {"_id": 0}
        ).sort("timestamp", 1)
    )

    return {
        "video_id": video_id,
        "user_email": user_email,
        "messages": chats
    }
