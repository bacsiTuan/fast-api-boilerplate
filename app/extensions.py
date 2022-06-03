#!/usr/bin/env python
# -*- coding: utf-8 -*-
from orm_alchemy import ActiveAlchemy
from app.config import config_app


db = ActiveAlchemy(config_app.DATABASE_URL, echo=config_app.SQLALCHEMY_ECHO)
