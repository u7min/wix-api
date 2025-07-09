import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware


dotenv_path = os.path.join(os.getcwd(), ".env")
if os.path.exists(dotenv_path):
    load_dotenv()

_openapi = FastAPI.openapi

app = FastAPI(
    title="Booding API",
    version="0.0.3",
    description="부딩 API for 데이터베이스 조회",
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/redoc")


from app.api.router.posts import router as posts_router
from app.api.router.articles import router as articles_router


async def startup_event():
    pass


async def shutdown_event():
    pass


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(posts_router)
app.include_router(articles_router)
