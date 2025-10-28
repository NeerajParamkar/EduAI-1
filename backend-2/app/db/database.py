from pymongo import MongoClient
from app.core.config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

users_collection = db["users"]
transcripts_collection = db["transcripts"]
chats_collection = db["chats"] 