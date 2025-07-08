import os

from fastapi import Header


API_USER = os.getenv("X_API_USER")
API_ADMN = os.getenv("X_API_ADMN")


async def verify_user(x_api_user: str = Header(None)):
    return x_api_user != API_USER and x_api_user != API_ADMN


async def verify_admin(x_api_user: str = Header(None)):
    return x_api_user != API_ADMN
