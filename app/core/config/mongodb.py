from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from app.utils.logger import logger

load_dotenv()
mongo_client = None

if os.getenv("MONGODB_URI") is None:
    raise Exception("MONGODB_URI is not set")

try:
    if mongo_client is None:
        mongo_client = AsyncIOMotorClient(
            os.getenv("MONGODB_URI"), server_api=ServerApi("1")
        )
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
