import asyncio
from fastapi import APIRouter, Header, status

from app.api.auth_verifier import verify_admin
from app.api.exception.custom_exception import CustomException
from app.api.exception.error_code import ErrorCode
from app.api.models import BaseResponse
from app.api.mongo import wix
from app.api.service.wix_api import fetch_all_posts
from app.api.service.wix_scraper import convert_all_scraps_to_markdown


router = APIRouter()
posts_collection = wix["posts"]


@router.post("/posts/fetchAll", response_model=BaseResponse, include_in_schema=False)
async def fetch_all(
    x_api_user: str = Header(None),
):
    """
    Wix API 를 통해 전체 Booding 의 전체 Post 의 Meta 데이터를 가져와서 posts 에 저장 합니다.
    """
    verify = await verify_admin(x_api_user)
    if not verify:
        raise CustomException(
            error_code=ErrorCode.BAD_REQUEST,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="x-api-user is unauthorized.",
        )
    asyncio.create_task(fetch_all_posts())
    response = {
        "message": "Fetch started.",
        "ok": True,
    }
    return response


@router.post("/posts/scrapAll", response_model=BaseResponse, include_in_schema=False)
async def scrap_all(x_api_user: str = Header(None)):
    """
    Wix HTTP 를 통해 Booding 의 전체 Post 콘텐츠를 스크랩 해 와서 articles 에 저장 합니다.
    """
    verify = await verify_admin(x_api_user)
    if not verify:
        raise CustomException(
            error_code=ErrorCode.BAD_REQUEST,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="x-api-user is not verified.",
        )
    asyncio.create_task(
        convert_all_scraps_to_markdown(
            test_one=False,
        )
    )
    response = {
        "message": "Scrap started.",
        "ok": True,
    }
    return response
