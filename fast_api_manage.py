#!/usr/bin/env python
# coding: utf8
import os

from dotenv import load_dotenv
from fast_api_app import create_app

load_dotenv(override=False)

application = app = create_app()
