import os
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = 15
MAX_RETRIES = 3
VERSION = "2.1.0"
APP_NAME = "R10 Web X-RAY Bot"
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")