#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kafka_app._enum import KafkaType
from kafka_app.consumer import KafkaConsumer
from kafka_app.producer import KafkaProducer


class KafkaFactory(object):
    @classmethod
    def create(cls, kafka_type: KafkaType, url: str, configs: object) -> object:
        if kafka_type == KafkaType.PRODUCER:
            return KafkaProducer(url, configs)
        elif kafka_type == KafkaType.CONSUMER:
            return KafkaConsumer(url, configs)
        return None
