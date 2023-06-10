#!/usr/bin/env python
# -*- coding: utf-8 -*-
from orm_alchemy import ActiveAlchemy
from app.config import config_app, ConfigKafka
import os
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging
import mongoengine
import redis
from kafka_app import KafkaType, KafkaFactory

db = ActiveAlchemy(config_app.DATABASE_URL, echo=config_app.SQLALCHEMY_ECHO)
db_mongo = mongoengine.connect(host=config_app.MONGODB_URL)

redis_client = redis.Redis(
    host=config_app.REDIS.REDIS_HOST,
    port=int(config_app.REDIS.REDIS_PORT),
    password=config_app.REDIS.REDIS_PASSWORD,
    # db=int(config_app.REDIS.REDIS_DB),
    decode_responses=True,
)

# Set up a Kafka producer.
kafka_producer = KafkaFactory.create(
    KafkaType.PRODUCER, ConfigKafka.KAFKA_URL, config_app
)

# set up sentry
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=None,  # Send errors as events
)


# remove spam error messages
def strip_sensitive_data(event, hint):
    # modify event here
    if event.get("level") == "error":
        return None
    return event


SENTRY_DSN = os.environ.get("SENTRY_DSN") or None
sentry_sdk.init(
    dsn=SENTRY_DSN,
    debug=False,
    integrations=[
        sentry_logging,
    ],
    before_send=strip_sensitive_data,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=0,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)
