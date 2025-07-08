import os
import httpx
import asyncio
import html2text
from bs4 import BeautifulSoup

from app.api.mongo import wix


BOODING_BASE_URL = os.getenv("BOODING_BASE_URL")

posts_collection = wix["posts"]
articles_collection = wix["articles"]


async def scrap_article_markdown(slug: str, id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BOODING_BASE_URL}{slug}")
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("article")
    if not article:
        print(f"❌ article not found for {slug}")
        return None

    html_content = str(article)
    markdown = html2text.html2text(html_content)

    doc = await posts_collection.find_one({"id": id})
    if not doc:
        print(f"❌ post not found for {slug}")
        return None

    title = doc.get("title", "")
    firstPublishedDate = doc.get("firstPublishedDate", "")
    lastPublishedDate = doc.get("lastPublishedDate", "")

    await articles_collection.update_one(
        {"id": id},
        {
            "$set": {
                "slug": slug,
                "id": id,
                "title": title,
                "firstPublishedDate": firstPublishedDate,
                "lastPublishedDate": lastPublishedDate,
                "markdown": markdown,
            },
        },
        upsert=True,
    )
    print(f"✅ saved markdown for {slug}")


async def convert_all_scraps_to_markdown(
    delay: float = 1.0,
    test_one: bool = False,  # test_one = True 설정 시 1건 실행 후 종료
):
    cursor = posts_collection.find({}, {"slug": 1, "id": 1})
    async for doc in cursor:
        slug = doc.get("slug")
        id = doc.get("id")
        if slug and id:
            await scrap_article_markdown(slug, id)
            if test_one:
                break
            await asyncio.sleep(delay)
