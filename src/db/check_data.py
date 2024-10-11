import asyncio

from aiogram import types
from aiogram.types import Message

from config import bot, logger


async def get_data_url(message: types.Message):
    """Checking the message for additional files"""
    files = ""

    try:
        if message.document:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
            files += file_url + "\n"
            logger.info(f"Document: {file_url}")

        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
            files += file_url + "\n"
            logger.info(f"Photo: {file_url}")

        if message.video:
            file_id = message.video.file_id
            file = await bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
            files += file_url + "\n"
            logger.info(f"Video: {file_url}")

        if not files:
            logger.info("No attachments found in the message.")

        logger.info(files)
    except Exception as err:
        logger.error(f"{err}")

    return files
