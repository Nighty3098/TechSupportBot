import asyncio
import logging
from typing import Any, Coroutine, List, Tuple, Optional

from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from config import CHANNEL, DEVS, TOKEN, bot, data, dp, log_file, logger
from db.db import (
    create_connection,
    get_all_tickets,
    get_ticket_status,
    get_user_id_by_message,
    save_report_data,
    update_ticket_status,
)
from get_admins_id import get_users
from kb_builder import back_btn, main_kb
from resources.TEXT_MESSAGES import (
    BUG_TEXT,
    DEVS_TEXT,
    DONE_TEXT,
    HELLO_MESSAGE,
    HELP_MESSAGE,
    IDEA_TEXT,
    INCORRECT_INPUT_FORMAT_ERROR,
    OUR_PRODUCTS_TEXT,
    SUPPORT_TEXT,
)
from send_data import send_messages
from send_logs import send_log_to_dev
from StatesGroup import GetBug, GetIdea

def admin_required(func: Coroutine) -> Coroutine:
    async def wrapper(message: Message, *args, **kwargs) -> None:
        admins = await get_users()
        if message.from_user.id not in admins:
            logger.warning(
                f"Unauthorized access attempt by {message.from_user.username} ({message.from_user.id})"
            )
            return
        return await func(message, *args, **kwargs)
    return wrapper

def error_handler(func: Coroutine) -> Coroutine:
    async def wrapper(*args: Any, **kwargs: Any) -> None:
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            logger.error(f"Error in {func.__name__}: {err}", exc_info=True)
            await send_log_to_dev()
    return wrapper

async def send_photo_message(
    chat_id: int, 
    image_path: str, 
    caption: str, 
    parse_mode: str = "MarkdownV2",
    reply_markup: Optional[types.InlineKeyboardMarkup] = None
) -> None:
    await bot.send_photo(
        chat_id=chat_id,
        photo=FSInputFile(image_path),
        caption=caption,
        parse_mode=parse_mode,
        reply_markup=reply_markup
    )

async def parse_command_args(message: Message, expected_parts: int) -> Tuple[str, ...]:
    parts = message.text.split(" | ")
    if len(parts) != expected_parts:
        logger.error(INCORRECT_INPUT_FORMAT_ERROR)
        raise ValueError(INCORRECT_INPUT_FORMAT_ERROR)
    return tuple(parts)

@dp.message(Command("admin_answer"))
@error_handler
@admin_required
async def send_admin_answer(message: Message) -> None:
    parts = await parse_command_args(message, 3)
    _, client_id, source_message = parts
    
    asyncio.create_task(process_admin_answer(client_id, source_message))
    await message.answer("✅ Message successfully delivered")

@dp.message(Command("set_ticket_status"))
@error_handler
@admin_required
async def set_ticket_status(message: Message) -> None:
    parts = await parse_command_args(message, 4)
    _, ticket_id, ticket_category, new_status = parts
    
    asyncio.create_task(
        process_ticket_status_update(ticket_id, new_status, ticket_category)
    )
    await message.answer("🔥 Ticket status has been successfully updated")

@dp.message(Command("get_ticket_status"))
@error_handler
@admin_required
async def get_status(message: Message) -> None:
    parts = await parse_command_args(message, 3)
    _, ticket_id, ticket_category = parts
    
    async with create_connection() as conn:
        ticket_status = await get_ticket_status(conn, ticket_id, ticket_category)
    
    response = (
        f"The current status of the ticket is: {ticket_status}\n\n"
        f"To change the status enter:\n"
        f"`/set_ticket_status | {ticket_id} | {ticket_category.lower()} | Ticket status`"
    )
    await message.answer(response, parse_mode="MarkdownV2")

@dp.message(Command("get_all_tickets"))
@error_handler
@admin_required
async def get_tickets(message: Message) -> None:
    async with create_connection() as conn:
        tickets = await get_all_tickets(conn)
    
    ticket_messages = [
        f"ID: {t['id']}\nCategory: {t['category']}\nStatus: {t['status']}\n"
        f"User ID: {t['user_id']}\nUsername: @{t['username']}\nMessage:\n{t['message']}"
        for t in tickets
    ]
    
    if not ticket_messages:
        await message.answer("No data available")
        return
    
    with open("AllTickets.txt", "w", encoding="utf-8") as f:
        f.write("\n\n\n\n\n".join(ticket_messages))
    
    await bot.send_chat_action(message.chat.id, "upload_document")
    await message.answer_document(
        FSInputFile("AllTickets.txt"),
        caption="👾 *_All tickets_* 👾",
        parse_mode="MarkdownV2"
    )

@dp.message(Command("get_db"))
@error_handler
@admin_required
async def get_db(message: Message) -> None:
    try:
        await bot.send_chat_action(message.chat.id, "upload_document")
        await message.answer_document(
            FSInputFile(data), 
            caption="👾 DXS GROUP DB 👾"
        )
    except FileNotFoundError:
        await message.answer("DB File not found.")

@dp.message(Command("help"))
@error_handler
@admin_required
async def get_help(message: Message) -> None:
    await send_photo_message(
        message.chat.id,
        "resources/header_2.png",
        HELP_MESSAGE,
        reply_markup=await main_kb()
    )

async def process_admin_answer(client_id: str, source_message: str) -> None:
    try:
        await send_photo_message(
            int(client_id),
            "resources/header_2.png",
            f"🔥 Message from admin:\n\n{source_message}"
        )
    except Exception as err:
        logger.error(f"Error sending admin answer: {err}")
        await send_log_to_dev()

async def process_ticket_status_update(
    ticket_id: str,
    new_status: str,
    ticket_category: str
) -> None:
    try:
        async with create_connection() as conn:
            client_id = await get_user_id_by_message(conn, ticket_id, ticket_category)
            await update_ticket_status(conn, ticket_id, new_status, ticket_category)
        
        await send_photo_message(
            int(client_id),
            "resources/header_2.png",
            f"🚀 The status of your ticket has been updated to:\n\n{new_status}"
        )
    except Exception as err:
        logger.error(f"Error updating ticket status: {err}")
        await send_log_to_dev()
