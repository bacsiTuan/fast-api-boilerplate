#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import socket

from kafka import KafkaAdminClient  # noqa
from kafka import KafkaProducer as KafkaProducerCore  # noqa
from kafka.admin import NewTopic  # noqa
from loguru import logger

from kafka_app.base import KafkaBase


def on_success(record_metadata):
    logger.info(record_metadata.topic)
    logger.info(record_metadata.partition)
    logger.info(record_metadata.offset)


def on_error(exception):
    logger.error("Kafka Error: ", exc_info=exception)


class KafkaProducer(KafkaBase):
    def push(self, topic, message) -> bool:
        producer = None
        success = False
        try:
            producer = KafkaProducerCore(
                bootstrap_servers=self.bootstrap_servers,
                client_id=socket.gethostname(),
                request_timeout_ms=2000,
                api_version=(2, 3, 0),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )

            producer.send(topic, message).add_callback(on_success).add_errback(on_error)
            producer.flush()
            success = True
        except Exception as e:
            logger.exception(e)
        finally:
            if producer:
                producer.close()
            return success
