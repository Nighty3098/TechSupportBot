import os
import sys

import loguru
import pretty_errors
import aiogram.enums 
import aiogram.filters 
import aiogram.types
import aiogram.utils.markdown 
from aiogram import * 

home_dir = os.environ['HOME']
TOKEN = os.getenv("SUPPORT_TOKEN")
log_file = home_dir + "/logs/TechSupport.log"
data = home_dir + "/TechSupport.db"

DEVS = ["1660218648"]

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
    rotation="10000 MB",
    retention="7 days",
    backtrace=True,
    diagnose=True,
)