from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.api.exception.error_code import ErrorCode
from app.api.main import app


class CustomExceptionResponse(BaseModel):
    message: str
    error_code: ErrorCode


class CustomException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_200_OK,
        error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
        message: str = "",
        ok: bool = False,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.ok = ok


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, ex: CustomException):
    print(f"Exception raised: ${ex.error_code} {ex.message}")
    return JSONResponse(
        status_code=ex.status_code,
        content=jsonable_encoder(
            {
                "ok": ex.ok,
                "message": f"{ex.message}",
                "error_code": ex.error_code,
            }
        ),
    )
