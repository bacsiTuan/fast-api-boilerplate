#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger

from app.decorators import sqlalchemy_session
from app import models as m
from app.extensions import db, kafka_producer
from app.repositories.tasks import tasks_repo
from app.config import ConfigKafka


class TasksService(object):
    @classmethod
    @sqlalchemy_session(db)
    def create_task(cls, **kwargs):
        task = tasks_repo.create(**kwargs)
        publish = kafka_producer.push(
            ConfigKafka.TOPIC,
            {
                "type": "ADD_MONGO",
                "payload": {
                    "voucher_detail_id": 2,
                },
            },
        )
        logger.info(publish)
        return task.json

    @classmethod
    def add_mongo(cls, request=None):
        logger.info(request)
        booking_log = m.MBookingLog(
            booking_id=1111,
            store_id=12,
            check_code="abc"
        )
        booking_log.save()
        return True
