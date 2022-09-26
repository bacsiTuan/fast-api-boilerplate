from typing import Any
from loguru import logger
from fastapi import APIRouter, Request, Body
from app.api.redis_service import RedisService

router = APIRouter()


@router.get("/redis-stream", status_code=200)
def login_access_token() -> Any:
    RedisService.stream()
    return {"ping": "pong1"}
