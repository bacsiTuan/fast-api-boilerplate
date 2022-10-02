#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py_header_lib.grpc_services.common.proto.ping_pb2_grpc import APIPingServicer
from py_header_lib.grpc_services.common.proto.ping_pb2 import PingReply


class APIPing(APIPingServicer):
    def Ping(self, request, context):
        print(request)
        print(context)
        return PingReply(message="pong")
