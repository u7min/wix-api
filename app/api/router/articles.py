from fastapi import APIRouter, Header, Query, status
from fastapi.responses import HTMLResponse, JSONResponse

from app.api.auth_verifier import verify_user
from app.api.exception.custom_exception import CustomException
from app.api.exception.error_code import ErrorCode
from app.api.models import ArticleListResponse, ArticleResponse
from app.api.mongo import wix
from app.api.utils import convert_dates_to_kst


router = APIRouter()
articles_collection = wix["articles"]


@router.get("/articles", response_model=ArticleListResponse)
async def get_article_list(
    x_api_user: str = Header(None),
    offset: int = Query(0),
    limit: int = Query(10),
):
    """
    부딩 Article 리스트를 조회 합니다.
    """
    verify = await verify_user(x_api_user)
    if not verify:
        raise CustomException(
            error_code=ErrorCode.BAD_REQUEST,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="x-api-user is unauthorized.",
        )
    docs = articles_collection.find().skip(offset).limit(limit)
    results = []
    async for doc in docs:
        doc["_id"] = str(doc["_id"])
        converted_doc = convert_dates_to_kst(
            doc, ["firstPublishedDate", "lastPublishedDate"]
        )
        results.append(converted_doc)

    response = {
        "message": "",
        "ok": True,
        "data": results,
    }
    return response


@router.get("/articles/{id}", response_model=ArticleResponse)
async def get_article_by_id(id: str, x_api_user: str = Header(None)):
    """
    부딩 Article 을 조회 합니다.
    """
    verify = await verify_user(x_api_user)
    if not verify:
        raise CustomException(
            error_code=ErrorCode.BAD_REQUEST,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="x-api-user is unauthorized.",
        )
    doc = await articles_collection.find_one({"id": id})
    if not doc:
        raise CustomException(
            error_code=ErrorCode.DATA_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            message="article not found.",
        )
    doc["_id"] = str(doc["_id"])
    converted_doc = convert_dates_to_kst(
        doc, ["firstPublishedDate", "lastPublishedDate"]
    )

    response = {
        "message": "",
        "ok": True,
        "data": converted_doc,
    }
    return response


@router.get("/articles/{id}/markdown", response_class=HTMLResponse)
async def get_article_markdown_by_id(id: str, x_api_user: str = Header(None)):
    """
    부딩 Article 을 조회 합니다. (MarkDown 을 HTML로 확인)
    """
    verify = await verify_user(x_api_user)
    if not verify:
        raise CustomException(
            error_code=ErrorCode.BAD_REQUEST,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="x-api-user is unauthorized.",
        )
    doc = await articles_collection.find_one({"id": id})
    if not doc:
        raise CustomException(
            error_code=ErrorCode.DATA_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            message="article not found.",
        )
    markdown_text = doc.get("markdown", "")
    escaped = (
        markdown_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>{doc.get("title")}</title>
    </head>
    <body>
        <pre>{escaped}</pre>
    </body>
    </html>
    """
