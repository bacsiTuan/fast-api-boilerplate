from datetime import timedelta
from typing import Any

from fastapi import APIRouter
from app.errors.exceptions import BadRequest,UrBoxException
import schemas
from fastapi import HTTPException
router = APIRouter()


@router.get("/login/access-token", status_code=201)
def login_access_token() -> Any:
    # raise BadRequest()
    raise HTTPException(status_code=400, detail="1")
    # return {
    #     "ping": "pong"
    # }
