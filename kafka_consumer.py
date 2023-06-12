#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger

from app.api.tasks import TasksService
from app.config import config_app
from kafka_app import KafkaFactory, KafkaType

configs = config_app
configs.FUNCTION_CONSUMER_SUBSCRIBE = {
    f"[{config_app.TOPIC}][ADD_MONGO]": TasksService.add_mongo,
}

logger.info("STARTED KAFKA WORKER... 🚛 🚛 🚛")

kafka_consumer = KafkaFactory.create(
    KafkaType.CONSUMER, config_app.KAFKA_URL, configs
)
kafka_consumer.start(config_app.KAFKA_GROUP)
