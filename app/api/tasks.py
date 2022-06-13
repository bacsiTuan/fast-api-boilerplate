#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger

from app.decorators import sqlalchemy_session
from app import models as m
from app.extensions import db
from app.repositories.tasks import tasks_repo


class TasksService(object):
    @classmethod
    @sqlalchemy_session(db)
    def create_task(cls, **kwargs):
        task = tasks_repo.create(**kwargs)
        return task.json

    @classmethod
    def add_mongo(cls):
        booking_log = m.MBookingLog(
            booking_id=1111,
            store_id=12,
        )
        booking_log.save()
        return True
