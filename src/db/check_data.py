from aiogram.types import Message
from aiogram import types
import asyncio

from config import logger, bot

async def get_data_url(message: types.Message):
    files = ""

    try:
        if message.document:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
            files += file_url + "\n"
            logger.debug(f"Document: {file_url}")

        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
            files += file_url + "\n"
            logger.debug(f"Photo: {file_url}")

        if message.video:
            file_id = message.video.file_id
            file = await bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
            files += file_url + "\n"
            logger.debug(f"Video: {file_url}")

        if not files:
            logger.debug("No attachments found in the message.")

        logger.debug(files)
    except Exception as err:
        logger.error(f"{err}")

    return files
