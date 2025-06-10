import os
import sys

import loguru
import pretty_errors
from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from dotenv import dotenv_values, load_dotenv

load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

home_dir = os.environ["HOME"]

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")
NOTIFY_CHAT = os.getenv("NOTIFY_CHAT")
DEVS = os.getenv("DEVS").split(",")

log_file = home_dir + "/logs/TechSupport.log"

bot = Bot(TOKEN)
dp = Dispatcher()

logger = loguru.logger

logger.level("DEBUG", color="<green>")
logger.level("INFO", color="<cyan>")
logger.level("WARNING", color="<yellow>")
logger.level("CRITICAL", color="<red>")

logger.add(
    log_file,
    level="DEBUG",
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    backtrace=True,
    diagnose=True,
)
