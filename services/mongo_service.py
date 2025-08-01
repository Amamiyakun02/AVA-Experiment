# services/mongo_service.py
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os

# Load .env
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
DB_NAME = os.getenv("MONGO_NAME")

# Setup MongoDB client
mongo_client = MongoClient(
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}{MONGO_URI}?retryWrites=true&w=majority&appName=aimer"
)
db = mongo_client[DB_NAME]

# Koleksi
users_col = db["users"]
memory_col = db["memory"]
chat_sessions_col = db["chatsessions"]
chat_messages_col = db["chatmessages"]

# ==== FUNGSI SERVIS ====

def get_user_by_id(user_id: str):
    return users_col.find_one({"user_id": user_id})

def save_chat_message(session_id: str, message: dict):
    message["session_id"] = session_id
    message["timestamp"] = datetime.utcnow()
    return chat_messages_col.insert_one(message)

def get_chat_history(session_id: str, limit=20):
    return list(chat_messages_col.find({"session_id": session_id}).sort("timestamp", -1).limit(limit))

def save_memory(user_id: str, memory_chunk: str, source: str = "user"):
    return memory_col.insert_one({
        "user_id": user_id,
        "text": memory_chunk,
        "source": source,
        "timestamp": datetime.utcnow()
    })

def get_all_memories(user_id: str):
    return list(memory_col.find({"user_id": user_id}))

def get_recent_memories(user_id: str, limit=5):
    return list(memory_col.find({"user_id": user_id}).sort("timestamp", -1).limit(limit))

def get_old_memories(user_id: str, cutoff_datetime):
    return list(memory_col.find({
        "user_id": user_id,
        "timestamp": {"$lt": cutoff_datetime}
    }))
