from fastapi import FastAPI, APIRouter

from fast_api_app.api_v1 import login


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"], prefix="/login")
