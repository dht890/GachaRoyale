from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client['game']

cards_collection = db['cards']
users_collection = db["profiles"]
chests_collection = db['chests']

