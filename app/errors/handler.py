#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from loguru import logger
from werkzeug.exceptions import HTTPException

from app.errors.exceptions import UrBoxException


def api_error_handler(error):
    if isinstance(error, UrBoxException):
        logger.warning(f"HTTP_STATUS_CODE: {error.status_code.value} - {error.to_dict}")
        return jsonable_encoder(error.to_dict), error.status_code.value

    if isinstance(error, HTTPException):
        return (
            jsonable_encoder({"error": {"code": error.code, "message": error.description}}),
            error.code,
        )

    logger.exception(error)
    return jsonable_encoder({"error": {"code": 500, "message": "Internal Server Error"}}), 500
