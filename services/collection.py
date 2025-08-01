from pymongo import MongoClient
from dotenv import load_dotenv
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
contacts_col = db["contacts"]
