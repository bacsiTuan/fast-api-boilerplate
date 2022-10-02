from fastapi import FastAPI, APIRouter

from fast_api_app.api_v1 import login, redis


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"], prefix="/login")
api_router.include_router(redis.router, tags=["redis"], prefix="/redis")

