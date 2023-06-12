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
    API_V2_STR: str = "/api/v2"
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
    # config mysql
    # DB_TYPE = os.environ.get("DB_MYSQL_TYPE") or "mysql"
    # DB_CONNECTOR = os.environ.get("DB_MYSQL_CONNECTOR") or "pymysql"
    # DB_USERNAME = os.environ.get("DB_MYSQL_USER")
    # DB_PASSWORD = os.environ.get("DB_MYSQL_PASS")
    # DB_HOST = os.environ.get("DB_MYSQL_HOST")
    # DB_PORT = os.environ.get("DB_MYSQL_PORT")
    # DB_NAME = os.environ.get("DB_MYSQL_DBNAME")

    # config postgres
    DB_TYPE = os.environ.get("DB_PG_TYPE") or "postgresql"
    DB_CONNECTOR = os.environ.get("DB_PG_CONNECTOR") or "psycopg2"
    DB_USERNAME = os.environ.get("DB_PG_USER")
    DB_PASSWORD = os.environ.get("DB_PG_PASS")
    DB_HOST = os.environ.get("DB_PG_HOST")
    DB_PORT = os.environ.get("DB_PG_PORT")
    DB_NAME = os.environ.get("DB_PG_DBNAME")

    DATABASE_URL = f"{DB_TYPE}+{DB_CONNECTOR}://{urllib.parse.quote(str(DB_USERNAME))}:{urllib.parse.quote(str(DB_PASSWORD))}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class ConfigRedis(object):
    REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
    REDIS_PORT = os.environ.get("REDIS_PORT") or "6379"
    REDIS_DB = os.environ.get("REDIS_DB") or "6"
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD") or ""


class ConfigKafka(object):
    PREFIX = (os.environ.get("APP_CONFIG") or "UNKNOWN").upper()
    KAFKA_URL = os.environ.get("KAFKA_URL") or "kafka:9092"
    KAFKA_GROUP = f"{PREFIX}_GROUP_FASTAPI"
    TOPIC = f"{PREFIX}_TOPIC_FASTAPI"
    INSTANCE_TOPICS = [TOPIC]


class ConfigMongoDB(object):
    MONGODB_HOST = os.environ.get("DB_MONGO_HOST") or "<your mongodb host>"
    MONGODB_PORT = int(os.environ.get("DB_MONGO_PORT") or "27017")
    MONGODB_DB = os.environ.get("DB_MONGO_DATABASE") or "<your mongodb database>"
    MONGODB_USERNAME = os.environ.get('DB_MONGO_USERNAME') or None
    MONGODB_PASSWORD = os.environ.get('DB_MONGO_PASSWORD') or None
    MONGODB_REPLICASET = os.environ.get('DB_MONGODB_REPLICASET') or None  # 'rs0'
    MONGODB_READ_PREFERENCE = os.environ.get('MONGODB_READ_PREFERENCE') or None
    MONGODB_RETRY_WRITES = os.environ.get("DB_MONGO_RETRY_WRITES") or 'false'
    IS_MONGO_SRV = os.environ.get("DB_MONGO_SRV") or "NO"

    MONGODB_URL = f'mongodb://'
    if IS_MONGO_SRV == "YES":
        MONGODB_URL = f'mongodb+srv://'
    if MONGODB_USERNAME is not None and MONGODB_PASSWORD is not None and IS_MONGO_SRV == "NO":
        MONGODB_URL = f'{MONGODB_URL}{urllib.parse.quote(MONGODB_USERNAME)}:{urllib.parse.quote(MONGODB_PASSWORD)}@{MONGODB_HOST}:{MONGODB_PORT}/'
    elif MONGODB_USERNAME is not None and MONGODB_PASSWORD is not None and IS_MONGO_SRV == "YES":
        MONGODB_URL = f'{MONGODB_URL}{urllib.parse.quote(MONGODB_USERNAME)}:{urllib.parse.quote(MONGODB_PASSWORD)}@{MONGODB_HOST}/'
    else:
        MONGODB_URL = f'{MONGODB_URL}{MONGODB_HOST}:{MONGODB_PORT}/'

    if MONGODB_DB is not None:
        MONGODB_URL = f'{MONGODB_URL}{MONGODB_DB}'
    MONGODB_URL = f'{MONGODB_URL}?retryWrites={MONGODB_RETRY_WRITES}'
    if MONGODB_READ_PREFERENCE is not None:
        MONGODB_URL = f'{MONGODB_URL}&readPreference={MONGODB_READ_PREFERENCE}'
    if MONGODB_REPLICASET is not None:
        MONGODB_URL = f'{MONGODB_URL}&replicaSet={MONGODB_REPLICASET}'


class Config(ConfigMysql, ConfigMongoDB, ConfigRedis, ConfigKafka):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "<your secret key>"
    REDIS = ConfigRedis()


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
