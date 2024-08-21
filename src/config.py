import os
import sys

import loguru
import pretty_errors
from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher

"""
Only for linux or mac
"""
home_dir = os.environ["HOME"]
TOKEN = os.getenv("SUPPORT_TOKEN")
log_file = home_dir + "/logs/TechSupport.log"
data = home_dir + "/TechSupport/TechSupport.db"

"""
for windows:
TOKEN = "TOKEN"
log_file = "logs/TechSupport.log"
data = TechSupport.db"
"""

DEVS = ["1660218648"]
CHANNEL = "-1002237746780"

NOTIFY_CHAT = "1660218648"

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
    rotation="500 MB",
    retention="30 days",
    backtrace=True,
    diagnose=True,
)
