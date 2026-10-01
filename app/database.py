from pymongo import MongoClient
from app.config import MONGO_URL, DATABASE

client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
def get_db():
    return client[DATABASE]
