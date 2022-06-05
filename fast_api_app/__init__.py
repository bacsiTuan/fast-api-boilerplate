from fast_api_app.api_v1 import app
from loguru import logger


def create_app():
    __config_logging(app)
    return app


def __config_logging(app):
    logger.info('Start fast api... 🚀🚀')
