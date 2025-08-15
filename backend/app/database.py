# backend/app/database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()   # reads ../.env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "whatsease_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]
messages_col = db["messages"]
logs_col = db["activity_logs"]
