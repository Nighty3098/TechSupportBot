import asyncio
import datetime
from typing import Any, Coroutine

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from config import bot, dp, logger
from db.db import create_connection, save_report_data
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

def error_handler(func: Coroutine) -> Coroutine:
    async def wrapper(*args: Any, **kwargs: Any) -> None:
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            logger.error(f"Error in {func.__name__}: {err}", exc_info=True)
            await send_log_to_dev()
    return wrapper

async def handle_report(
    message: Message,
    state: FSMContext,
    report_type: str,
    text: str
) -> None:
    username = message.from_user.username
    user_id = message.from_user.id
    logger.info(f"{report_type} from {username}: {text}")

    current_datetime = datetime.datetime.now()
    responsdate = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

    async with await create_connection() as connection:
        await save_report_data(
            connection=connection,
            username=username,
            user_id=str(user_id),
            message=message,
            label=report_type.upper(),
        )

    asyncio.create_task(
        send_messages(message, username, report_type.upper(), responsdate)
    )

    await message.answer_photo(
        photo=FSInputFile("resources/header_2.png"),
        caption=DONE_TEXT,
        reply_markup=await back_btn(),
        parse_mode="MarkdownV2",
    )
    await state.clear()

async def request_input(
    callback: types.CallbackQuery,
    state: FSMContext,
    text: str,
    next_state: Any
) -> None:
    await state.set_state(next_state)
    await state.update_data(last_bot_message_id=callback.message.message_id)

    await callback.message.edit_caption(
        caption=text,
        reply_markup=await back_btn(),
        parse_mode="MarkdownV2"
    )

@dp.callback_query(F.data == "SuggestIdea")
@error_handler
async def get_users_idea(callback: types.CallbackQuery, state: FSMContext) -> None:
    logger.info(f"{callback.message.chat.id} - idea suggest")
    await request_input(callback, state, IDEA_TEXT, GetIdea.wait_for_message)

@dp.callback_query(F.data == "BugReport")
@error_handler
async def get_users_bug(callback: types.CallbackQuery, state: FSMContext) -> None:
    logger.info(f"{callback.message.chat.id} - bug report")
    await request_input(callback, state, BUG_TEXT, GetBug.wait_for_message)

@dp.message(GetIdea.wait_for_message)
@error_handler
async def user_message_idea(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await bot.delete_message(message.chat.id, data["last_bot_message_id"])
    await handle_report(message, state, "SUGGESTION", message.text)

@dp.message(GetBug.wait_for_message)
@error_handler
async def user_message_bug(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await bot.delete_message(message.chat.id, data["last_bot_message_id"])
    await handle_report(message, state, "BUG", message.text)

@dp.callback_query(F.data == "Back")
@error_handler
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext) -> None:
    logger.info(f"{callback.message.chat.id} - back button")
    await state.clear()
    
    await callback.message.edit_caption(
        caption=HELLO_MESSAGE,
        reply_markup=await main_kb(),
        parse_mode="MarkdownV2",
    )

@dp.callback_query(F.data == "Contacts")
@error_handler
async def contacts(callback: types.CallbackQuery) -> None:
    logger.info(f"{callback.from_user.id} - contacts")
    await callback.message.edit_caption(
        caption=DEVS_TEXT,
        reply_markup=await contacts_btn(),
        parse_mode="MarkdownV2",
    )

@dp.callback_query(F.data == "OurProducts")
@error_handler
async def our_products(callback: types.CallbackQuery) -> None:
    logger.info(f"{callback.from_user.id} - our products")
    await callback.message.edit_caption(
        caption=OUR_PRODUCTS_TEXT,
        reply_markup=await back_btn(),
        parse_mode="MarkdownV2",
    )

@dp.callback_query(F.data == "SupportMe")
@error_handler
async def support_me(callback: types.CallbackQuery) -> None:
    logger.info(f"{callback.from_user.id} - support me")
    await callback.message.edit_caption(
        caption=SUPPORT_TEXT,
        reply_markup=await back_btn(),
        parse_mode="MarkdownV2",
    )
