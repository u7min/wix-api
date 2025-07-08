import os
from dotenv import load_dotenv
import httpx
import asyncio

from app.api.mongo import wix

dotenv_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv()

WIX_API_URL = os.getenv("WIX_API_URL")
WIX_API_TOKEN = os.getenv("WIX_API_TOKEN")
WIX_API_SITE_ID = os.getenv("WIX_API_SITE_ID")
WIX_API_HEADERS = {
    "Authorization": WIX_API_TOKEN,
    "wix-site-id": WIX_API_SITE_ID,
}

posts_collection = wix["posts"]


async def fetch_posts(offset: int, limit: int):
    async with httpx.AsyncClient() as client:
        if not WIX_API_URL:
            raise ValueError("WIX_API_URL environment variable is not set")
        response = await client.get(
            WIX_API_URL,
            headers={k: v for k, v in WIX_API_HEADERS.items() if v is not None},
            params={"paging.offset": offset, "paging.limit": limit},
        )
        response.raise_for_status()
        return response.json()


async def save_posts(posts: list):
    for post in posts:
        await posts_collection.update_one(
            {"id": post["id"]}, {"$set": post}, upsert=True
        )
    print(f"✅ {len(posts)} posts saved.")


async def fetch_all_posts():
    offset = 0
    limit = 100
    delay = 1
    total = 0
    while True:
        data = await fetch_posts(offset, limit)
        items = data.get("posts", [])
        if not items:
            print(f"🎉 Done. Total {total} posts processed.")
            break
        await save_posts(items)
        offset += limit
        total += len(items)
        await asyncio.sleep(delay)
