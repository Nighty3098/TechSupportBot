import asyncio
import json
import logging
import re
import time
import requests

from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.enums.chat_action import ChatAction

from config import bot, logger, log_file, DEVS

async def send_log_to_dev():
    try:
        for DEV in DEVS:
            file = FSInputFile(log_file, filename="TechSupport.log")
            await bot.send_chat_action(chat_id=DEV, action=ChatAction.UPLOAD_DOCUMENT)
            await bot.send_document(chat_id=DEV, document=file, allow_sending_without_reply=True)
            logger.warning(f"Sending logs to dev: {DEV}")
    except Exception as err:
        logger.error(f"{err}")
