import os

from dotenv import load_dotenv
from fast_api_manage import create_app

load_dotenv(override=False)

application = app = create_app()
