#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grpc_app.server import GRPCServer
from py_header_lib.grpc_services.common.proto import ping_pb2_grpc
from grpc_app.api import APIPing  # noqa


def create_app(address="0.0.0.0", port=6001):
    server = GRPCServer(address, port)
    add_services(server.instance)
    return server


def add_services(server):
    ping_pb2_grpc.add_APIPingServicer_to_server(APIPing(), server)
