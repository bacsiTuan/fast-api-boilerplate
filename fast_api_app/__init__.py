from fast_api_app.api_v1 import app, api_router
from loguru import logger
from app.config import settings
from app.extensions import db
from starlette.middleware.cors import CORSMiddleware


def create_app():
    __config_cors_middleware(app)
    __config_logging(app)
    __register_api_router(app)
    __init_app(app)

    return app


def __config_logging(app) -> None:
    logger.info("Start fast api... 🚀🚀")


def __register_api_router(app) -> None:
    app.include_router(api_router, prefix=settings.API_V1_STR)


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
