import asyncio
import json
import logging

from aiogram import F, handlers, types
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.types.input_file import InputFile

from config import CHANNEL, DEVS, TOKEN, bot, data, dp, log_file, logger
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
        global user_id, message_id
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        member = await bot.get_chat_member(chat_id, user_id)
        username = member.user.username

        image_path = "resources/TechSupport.png"

        photo = FSInputFile(image_path)
        message_id = await message.answer_photo(
            photo, caption=HELLO_MESSAGE, reply_markup=await main_kb()
        )

        logger.debug(f"{user_id} - main menu")

        message_for_dev = "New user: @" + username

        connection = await create_connection()
        await create_table(connection)

        for DEV in DEVS:
            await bot.send_message(chat_id=DEV, text=message_for_dev)
        await send_log_to_dev()

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "SuggestIdea")
async def GetUserIdea(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(GetIdea.wait_for_message)

        logger.debug(f"{callback.message.chat.id} - idea suggest")

        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=IDEA_TEXT,
            reply_markup=await back_btn(),
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "BugReport")
async def GetUserBug(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(GetBug.wait_for_message)

        logger.debug(f"{callback.message.chat.id} - bug report")

        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=BUG_TEXT,
            reply_markup=await back_btn(),
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetIdea.wait_for_message)
async def IdeaUserMessage(message: Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.debug(f"Idea suggest from {username}: {message.text}")

        try:
            await send_messages(message, username, "🍀 IDEA 🍀")

            connection = await create_connection()
            await save_report_data(
                connection=connection,
                username=username,
                message=message,
                label="SUGGESTION",
                text_message=message.text,
            )
        except Exception as e:
            logging.error(f"Error forwarding message from {username} to {CHANNEL}: {e}")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetBug.wait_for_message)
async def BugUserMessage(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.debug(f"Bug report from {username}: {message.text}")

        try:
            await send_messages(message, username, "❌ BUG ❌")

            connection = await create_connection()
            await save_report_data(
                connection=connection,
                username=username,
                message=message,
                label="BUG",
                text_message=message.text,
            )
        except Exception as e:
            logging.error(f"Error forwarding message from {username} to {CHANNEL}: {e}")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "Back")
async def BackToStartMenu(callback: types.CallbackQuery):
    try:
        logger.debug(f"{callback.message.chat.id} - back button")

        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=HELLO_MESSAGE,
            reply_markup=await main_kb(),
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "Contacts")
async def Contacts(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - contacts")

        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=DEVS_TEXT,
            reply_markup=await back_btn(),
        )
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "OurProducts")
async def OurProducts(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - our products")

        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=OUR_PRODUCTS_TEXT,
            reply_markup=await back_btn(),
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "SupportMe")
async def SupportMe(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - support me")

        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=SUPPORT_TEXT,
            reply_markup=await back_btn(),
        )
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
