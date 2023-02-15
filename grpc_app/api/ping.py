#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_header_lib.grpc_services.common.proto.ping_pb2_grpc import APIPingServicer
from py_header_lib.grpc_services.common.proto.ping_pb2 import PingReply
from loguru import logger


class APIPing(APIPingServicer):
    def Ping(self, request, context):
        logger.info(request)
        logger.info(context)
        logger.info(1)
        return PingReply(message="pong ping")
