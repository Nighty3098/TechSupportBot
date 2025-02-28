import asyncio
import datetime
import json
import logging

from aiogram import F, handlers, types
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.types.input_file import InputFile

from config import CHANNEL, DEVS, TOKEN, bot, data, dp, log_file, logger
from db.db import create_connection, create_table, save_report_data
from kb_builder import back_btn, contacts_btn, main_kb
from resources.TEXT_MESSAGES import (
    BUG_TEXT,
    DEVS_TEXT,
    DONE_TEXT,
    HELLO_MESSAGE,
    IDEA_TEXT,
    OUR_PRODUCTS_TEXT,
    SUPPORT_TEXT,
)
from send_data import send_messages
from send_logs import send_log_to_dev
from StatesGroup import GetBug, GetIdea


@dp.callback_query(F.data == "SuggestIdea")
async def get_users_idea(callback: types.CallbackQuery, state: FSMContext):
    try:
        global last_bot_message_id

        await state.set_state(GetIdea.wait_for_message)
        logger.info(f"{callback.message.chat.id} - idea suggest")

        message_id = callback.message.message_id
        last_msg = await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=IDEA_TEXT,
            reply_markup=await back_btn(),
            parse_mode="MarkdownV2",
        )

        last_bot_message_id = last_msg.message_id

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "BugReport")
async def get_users_bug(callback: types.CallbackQuery, state: FSMContext):
    try:
        global last_bot_message_id

        await state.set_state(GetBug.wait_for_message)
        logger.info(f"{callback.message.chat.id} - bug report")

        message_id = callback.message.message_id

        last_msg = await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=BUG_TEXT,
            reply_markup=await back_btn(),
            parse_mode="MarkdownV2",
        )

        last_bot_message_id = last_msg.message_id

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetIdea.wait_for_message)
async def user_message_idea(message: Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.info(f"Idea suggest from {username}: {message.text}")

        current_datetime = datetime.datetime.now()
        responsdate = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

        connection = await create_connection()
        await save_report_data(
            connection=connection,
            username=username,
            user_id=str(message.from_user.id),
            message=message,
            label="SUGGESTION",
        )

        asyncio.create_task(send_messages(message, username, "IDEA", responsdate))

        photo = FSInputFile("resources/header.png")

        await bot.delete_message(
            chat_id=message.chat.id, message_id=last_bot_message_id
        )

        await message.answer_photo(
            photo=photo,
            caption=DONE_TEXT,
            reply_markup=await back_btn(),
            parse_mode="MarkdownV2",
        )

        logger.info(await state.set_state(GetBug.none_state))
        logger.info(await state.set_state(GetIdea.none_state))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetBug.wait_for_message)
async def user_message_bug(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.info(f"Bug report from {username}: {message.text}")

        current_datetime = datetime.datetime.now()
        responsdate = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

        connection = await create_connection()
        await save_report_data(
            connection=connection,
            username=username,
            user_id=str(message.from_user.id),
            message=message,
            label="BUG",
        )

        asyncio.create_task(send_messages(message, username, "BUG", responsdate))

        photo = FSInputFile("resources/header.png")

        await bot.delete_message(
            chat_id=message.chat.id, message_id=last_bot_message_id
        )

        await message.answer_photo(
            photo=photo,
            caption=DONE_TEXT,
            parse_mode="MarkdownV2",
            reply_markup=await back_btn(),
        )

        logger.info(await state.set_state(GetBug.none_state))
        logger.info(await state.set_state(GetIdea.none_state))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "Back")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    try:
        logger.info(f"{callback.message.chat.id} - back button")
        message_id = callback.message.message_id

        logger.info(await state.set_state(GetBug.none_state))
        logger.info(await state.set_state(GetIdea.none_state))

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=HELLO_MESSAGE,
            reply_markup=await main_kb(),
            parse_mode="MarkdownV2",
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "Contacts")
async def contacts(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        logger.info(f"{user_id} - contacts")
        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=DEVS_TEXT,
            reply_markup=await contacts_btn(),
            parse_mode="MarkdownV2",
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "OurProducts")
async def our_products(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        logger.info(f"{user_id} - our products")
        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=OUR_PRODUCTS_TEXT,
            reply_markup=await back_btn(),
            parse_mode="MarkdownV2",
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "SupportMe")
async def support_me(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        logger.info(f"{user_id} - support me")
        message_id = callback.message.message_id

        await bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=message_id,
            caption=SUPPORT_TEXT,
            reply_markup=await back_btn(),
            parse_mode="MarkdownV2",
        )

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
