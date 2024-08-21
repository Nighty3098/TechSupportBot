import asyncio
import json
import logging
import re
import time
import requests

from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.enums.chat_action import ChatAction

from config import bot, logger, log_file, NOTIFY_CHAT

async def send_log_to_dev():
    try:
        file = FSInputFile(log_file, filename="TechSupport.log")
        await bot.send_chat_action(chat_id=NOTIFY_CHAT, action=ChatAction.UPLOAD_DOCUMENT)
        await bot.send_document(chat_id=NOTIFY_CHAT, document=file, allow_sending_without_reply=True)
        logger.warning(f"Sending logs to dev: {NOTIFY_CHAT}")
    except Exception as err:
        logger.error(f"{err}")
