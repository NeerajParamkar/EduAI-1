from pymongo import MongoClient
from app.core.config import MONGO_URI, DATABASE_NAME
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

users_collection = db["users"]
transcripts_collection = db["transcripts"]
chat_collection = db["chat_history"] 