import asyncio
import json
import logging

from aiogram import F, handlers, types
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.types.input_file import InputFile

from admin import send_admin_answer
from client import (back_to_menu, contacts, get_users_bug, get_users_idea,
                    support_me, user_message_bug, user_message_idea)
from config import CHANNEL, NOTIFY_CHAT, TOKEN, bot, data, dp, log_file, logger
from db.check_for_qsl_injection import is_sql_injection_attempt
from db.db import create_connection, create_table, save_report_data
from kb_builder import back_btn, main_kb
from resources.TEXT_MESSAGES import (BUG_TEXT, DEVS_TEXT, DONE_TEXT,
                                     HELLO_MESSAGE, IDEA_TEXT,
                                     OUR_PRODUCTS_TEXT, SUPPORT_TEXT)
from send_data import send_messages
from send_logs import send_log_to_dev
from StatesGroup import GetBug, GetIdea


@dp.message(CommandStart())
async def main_menu(message: Message) -> None:
    try:
        global user_id
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        member = await bot.get_chat_member(chat_id, user_id)
        username = member.user.username

        image_path = "resources/header.png"

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
