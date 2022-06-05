import secrets
from typing import Any, Dict, List, Optional, Union
# -*- coding: utf-8 -*-
import os
import urllib.parse
from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator
from loguru import logger
from dotenv import load_dotenv

load_dotenv(override=False)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "tuancong"
    SERVER_HOST: AnyHttpUrl = "http://0.0.0.0"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "FastAPI"

    class Config:
        case_sensitive = True


class ConfigMysql(object):
    SQLALCHEMY_ECHO = False
    DB_TYPE = os.environ.get("DB_MYSQL_TYPE") or "mysql"
    DB_CONNECTOR = os.environ.get("DB_MYSQL_CONNECTOR") or "pymysql"
    DB_USERNAME = os.environ.get("DB_MYSQL_USER")
    DB_PASSWORD = os.environ.get("DB_MYSQL_PASS")
    DB_HOST = os.environ.get("DB_MYSQL_HOST")
    DB_PORT = os.environ.get("DB_MYSQL_PORT")
    DB_NAME = os.environ.get("DB_MYSQL_DBNAME")
    DATABASE_URL = f"{DB_TYPE}+{DB_CONNECTOR}://{urllib.parse.quote(str(DB_USERNAME))}:{urllib.parse.quote(str(DB_PASSWORD))}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Config(ConfigMysql):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "<your secret key>"


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False


configs = {
    "develop": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
    "staging": ProductionConfig,
}

config_name = os.environ.get("APP_CONFIG") or "default"
config_app = configs[config_name]

settings = Settings()
