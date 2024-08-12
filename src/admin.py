import asyncio
import json
import logging

from aiogram import F, handlers, types
from aiogram.filters import CommandStart, Filter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.types.input_file import InputFile

from config import CHANNEL, DEVS, TOKEN, bot, data, dp, log_file, logger
from db.check_for_qsl_injection import is_sql_injection_attempt
from db.db import create_connection, create_table, save_report_data
from kb_builder import back_btn, main_kb
from resources.TEXT_MESSAGES import (BUG_TEXT, DEVS_TEXT, DONE_TEXT,
                                     HELLO_MESSAGE, IDEA_TEXT,
                                     OUR_PRODUCTS_TEXT, SUPPORT_TEXT)
from send_data import send_messages
from send_logs import send_log_to_dev
from StatesGroup import GetBug, GetIdea

from get_admins_id import get_users

@dp.message(Command("admin_answer"))
async def send_admin_answer(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(f"User {message.from_user.username} : {user_id} trying to exec admin_answer command")
        else:
            logger.warning(f"User: {message.from_user.username} : {user_id} - admin_answer")

            parts = message.text.split(" | ")

            if len(parts) != 3:
                logger.error("Incorrect input format")

            else:
                client_id = parts[1]
                source_message = parts[2]

                admin_message_text = f"🔥 Message from admin:\n{source_message}"

                await bot.send_message(chat_id=client_id, text=admin_message_text)

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
