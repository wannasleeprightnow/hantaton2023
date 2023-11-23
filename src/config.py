from os import environ

from dotenv import load_dotenv

load_dotenv()

DB_PATH = environ.get("DB_PATH")
TOKEN = environ.get("TELEGRAM_BOT_TOKEN")
