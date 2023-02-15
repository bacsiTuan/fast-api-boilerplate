#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

import grpc  # noqa
from loguru import logger

# from app.extensions import db


class GRPCServer(object):
    def __init__(self, address="[::]", port=50051):
        self.__address = address
        self.__port = port
        self.__server = grpc.server(ThreadPoolExecutor(max_workers=2))

        # def signalHandler(signal, frame):
        #     db.session.remove()
        #     if db.session.is_active:
        #         db.session.rollback()
        #
        #     logger.info("Process Interrupted!\n\a")
        #     self.__server.stop()
        #     sys.exit(0)
        #
        # signal.signal(signal.SIGINT, signalHandler)

    @property
    def instance(self):
        return self.__server

    def serve(self):
        endpoint = f"{self.__address}:{self.__port}"

        logger.info(f"Started GRPC Server at {endpoint}")
        logger.info("Serving GRPC... 🌋 🌋 🌋")

        self.__server.add_insecure_port(endpoint)
        self.__server.start()
        self.__server.wait_for_termination()

    def stop(self):
        logger.info("Stopping GRPC Server gracefully")
        self.__server.stop()
