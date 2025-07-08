from typing import List, Optional
from pydantic import BaseModel
from app.api.exception.error_code import ErrorCode


class Post(BaseModel):
    id: str = ""
    slug: str = ""
    title: str = ""
    firstPublishedDate: str = ""
    lastPublishedDate: str = ""


class Article(BaseModel):
    id: str = ""
    slug: str = ""
    title: str = ""
    firstPublishedDate: str = ""
    lastPublishedDate: str = ""
    markdown: str = ""


class BaseResponse(BaseModel):
    message: str
    ok: bool
    error_code: Optional[ErrorCode] = None


class ArticleResponse(BaseModel):
    message: str
    ok: bool
    data: Optional[Article] = None
    error_code: Optional[ErrorCode] = None


class ArticleListResponse(BaseModel):
    message: str
    ok: bool
    data: List[Article]
    error_code: Optional[ErrorCode] = None
