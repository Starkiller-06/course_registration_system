from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "course_registration")
class MongoDatabase:
    def __init__(self, uri= DB_URI, name=DB_NAME):
        self.client = MongoClient(uri)
        self.db = self.client[name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]