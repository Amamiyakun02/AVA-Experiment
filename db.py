from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
# Koneksi ke MongoDB lokal
MONGO_URI = os.getenv("MONGODB_URI")
mongo_user = os.getenv("MONGO_USER")
db_pass = os.getenv("MONGO_PASS")
db_name = os.getenv("MONGO_NAME")
client = MongoClient(f"mongodb+srv://{mongo_user}:{db_pass}{MONGO_URI}?retryWrites=true&w=majority&appName=aimer")

db = client[db_name]

users_col = db['users']
ltm_col = db['memory']


