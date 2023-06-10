#!/usr/bin/env python
# -*- coding: utf-8 -*-
import marshal

from kafka import KafkaAdminClient, TopicPartition, OffsetAndMetadata  # noqa
from kafka import KafkaConsumer as KafkaConsumerCore  # noqa
from kafka.admin import NewTopic  # noqa
from loguru import logger

from kafka_app.base import KafkaBase


class KafkaConsumer(KafkaBase):
    def start(self, group):
        consumer = KafkaConsumerCore(
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            value_deserializer=lambda v: marshal.loads(v),
            api_version=(2, 3, 0),
            group_id=f"{group}",
        )

        consumer.subscribe(self.instance_topics)

        for message in consumer:
            if message is None:
                continue

            message_topic = message.topic
            message_value = message.value
            message_type = message_value.get("type") or False
            message_payload = message_value.get("payload") or {}
            if not message_type:
                continue

            try:
                if (
                    f"[{message_topic}][{message_type}]"
                    not in self.configs.FUNCTION_CONSUMER_SUBSCRIBE
                ):
                    logger.error(
                        f"Không tìm thấy function config [{message_topic}][{message_type}]"
                    )
                    commit = True
                else:
                    try:
                        commit = self.configs.FUNCTION_CONSUMER_SUBSCRIBE[
                            f"[{message_topic}][{message_type}]"
                        ](message_payload)
                    except Exception as e:
                        logger.exception(e)
                        commit = True

                if commit or isinstance(commit, Exception):
                    topic_partition = TopicPartition(
                        topic=message.topic, partition=message.partition
                    )
                    offsets = {
                        topic_partition: OffsetAndMetadata(message.offset + 1, "")
                    }
                    consumer.commit(offsets)
            except Exception as e:
                logger.exception(e)

        return consumer
