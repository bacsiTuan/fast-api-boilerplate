#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from kafka import KafkaAdminClient  # noqa
from kafka.admin import NewTopic  # noqa


class KafkaBase(object):
    def __init__(self, url: str, configs: object):
        self.env = os.environ.get("APP_ENV")
        self.bootstrap_servers = url.split(",")
        self.instance_topics = configs.INSTANCE_TOPICS or []
        self.configs = configs or None
        self.check_topic()

    def check_topic(self):
        admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        broker_topics = admin_client.list_topics()

        topics = []

        # Make sure all topics that are to be used actually exist. This prevents
        # the consumer going into an infinite loop and 100% CPU usage when it
        # attempts to poll from a non-exising topic.
        # TODO: This will most probably be fixed in later versions of kafka_app-python
        for topic in self.instance_topics:
            if topic and topic not in broker_topics:
                print("Topic '%s' does not exist. Exiting!" % topic)
                topics = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]

        if len(topics) > 0:
            admin_client.create_topics(new_topics=topics, validate_only=False)
