from loguru import logger
from app.config import settings
from app.extensions import db
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def create_app():
    app = FastAPI(title="FastAPI", openapi_url=f"{settings.API_V1_STR}/openapi.json")
    __config_cors_middleware(app)
    __config_logging(app)
    __register_api_router(app)
    __init_app(app)

    return app


def __config_logging(app) -> None:
    logger.info("Start fast api... 🚀🚀")


def __register_api_router(app) -> None:
    from fast_api_app.api_v1 import api_router
    from fast_api_app.api_v2 import api_router_v2

    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(api_router_v2, prefix=settings.API_V2_STR)


def __init_app(app) -> None:
    db.init_app(app)


def __config_cors_middleware(app) -> None:
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
