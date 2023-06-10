#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum


class KafkaType(enum.Enum):
    PRODUCER = 1
    CONSUMER = 2
