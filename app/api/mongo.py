import os
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
wix = mongo_client["wix_blog"]
