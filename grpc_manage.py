#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from grpc_app import create_grpc_app
from dotenv import load_dotenv

load_dotenv(override=False)

grpc_host = os.environ.get("GRPC_HOST") or "0.0.0.0"
grpc_port = os.environ.get("GRPC_PORT") or "6001"
grpc_server = create_grpc_app(grpc_host, grpc_port)
grpc_server.serve()
