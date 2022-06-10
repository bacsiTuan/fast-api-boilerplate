from datetime import timedelta
from typing import Any
from loguru import logger
from fastapi import APIRouter, Request, Body
from app.errors.exceptions import BadRequest, CoreException
import schemas
from app.api.tasks import TasksService

router = APIRouter()


@router.get("/access-token", status_code=201)
def login_access_token() -> Any:
    # raise BadRequest(message="sai")
    # raise HTTPException(status_code=400, detail="1")
    return {"ping": "login v2"}


@router.post("/tasks", status_code=201)
def create_task(payload: dict = Body(...)):
    logger.info(payload)
    try:
        tasks = TasksService.create_task(**payload)
        return {"success": True, "data": tasks}
    except Exception as e:
        logger.error(e)
