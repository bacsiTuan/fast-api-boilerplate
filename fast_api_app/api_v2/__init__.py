from fastapi import FastAPI, APIRouter

from fast_api_app.api_v2 import login_v2


api_router_v2 = APIRouter()
api_router_v2.include_router(login_v2.router, tags=["login v2"], prefix="/login_v2")
