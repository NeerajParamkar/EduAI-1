# app/api/router_chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(prefix="/auth", tags=["Chat"])

# Temporary in-memory store (use DB later)
chat_memory = {}

class ChatMessage(BaseModel):
    video_id: str
    user_email: str
    message: str

class ChatHistoryResponse(BaseModel):
    video_id: str
    user_email: str
    messages: List[dict]

@router.post("/send_message")
def send_message(data: ChatMessage):
    key = f"{data.user_email}_{data.video_id}"
    if key not in chat_memory:
        chat_memory[key] = []
    # Save user question
    chat_memory[key].append({"role": "user", "text": data.message, "timestamp": datetime.now().isoformat()})
    
    # Generate mock AI response
    ai_text = f"That's an excellent question about '{data.message}'. Here's what I can explain..."
    chat_memory[key].append({"role": "ai", "text": ai_text, "timestamp": datetime.now().isoformat()})
    
    return {"status": "success", "response": ai_text, "timestamp": datetime.now().isoformat()}

@router.get("/get_chat_history")
def get_chat_history(video_id: str, user_email: str):
    key = f"{user_email}_{video_id}"
    if key not in chat_memory:
        return {"messages": []}
    return {"messages": chat_memory[key]}
