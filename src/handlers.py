import asyncio
import json
import logging

from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from config import NOTIFY_CHAT, bot, dp, logger
from db.db import create_connection, create_table
from kb_builder import main_kb
from resources.TEXT_MESSAGES import (
    HELLO_MESSAGE,
)
from send_logs import send_log_to_dev


@dp.message(CommandStart())
async def main_menu(message: Message) -> None:
    try:
        global user_id
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        member = await bot.get_chat_member(chat_id, user_id)
        username = member.user.username

        image_path = "resources/header_2.png"

        photo = FSInputFile(image_path)
        await message.answer_photo(
            photo,
            caption=HELLO_MESSAGE,
            reply_markup=await main_kb(),
            parse_mode="MarkdownV2",
        )

        logger.info(f"{user_id} - main menu")

        message_for_dev = "New user: @" + username

        connection = await create_connection()
        await create_table(connection)

        await bot.send_message(chat_id=NOTIFY_CHAT, text=message_for_dev)

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
