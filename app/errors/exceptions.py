#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.inum import HTTPStatusCode
from fastapi import HTTPException


class UrBoxException(HTTPException):
    status_code = HTTPStatusCode.SERVER_ERROR_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"

    def __init__(self, code=None, message=None):
        self.status_code = code or self.__class__.status_code
        self.detail = message or self.__class__.message

    @property
    def to_dict(self) -> dict:
        return {
            "error": {
                "message": self.message,
                "code": self.status_code.value
                if type(self.status_code) == HTTPStatusCode
                else self.status_code,
            }
        }



class BadRequest(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_BAD_REQUEST.value
    message = "Bad Request"


class NotFound(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_NOT_FOUND.value
    message = "Not Found"


class MethodNotAllowed(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_METHOD_NOT_ALLOWED.value
    message = "Method Not Allowed"


class UnSupportedMediaType(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_UNSUPPORTED_MEDIA_TYPE.value
    message = "Unsupported Media Type"


class Unauthorized(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_UNAUTHORIZED.value
    message = "Unauthorized"


class RequestTimeOut(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_REQUEST_TIME_OUT.value
    message = "Request Time Out"


class Forbidden(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_FORBIDDEN.value
    message = "Forbidden"


class ExceptionFailed(UrBoxException):
    status_code = HTTPStatusCode.CLIENT_ERROR_EXPECTATION_FAILED.value
    message = "Exception Failed"
