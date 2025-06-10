import asyncio
import logging
from typing import Any, Coroutine, List, Tuple, Optional

from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram import Dispatcher

from config import CHANNEL, DEVS, TOKEN, bot, logger
from db.crud import (
    get_all_tickets,
    get_ticket_status,
    get_user_id_by_message,
    update_ticket_status,
)
from db.database import get_session
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
    async def wrapper(message: Message, *args, **kwargs) -> None:
        try:
            return await func(message, *args, **kwargs)
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

async def get_help(message: Message, **kwargs) -> None:
    """Обработчик команды /help"""
    await send_photo_message(
        message.chat.id,
        "src/resources/header_2.png",
        HELP_MESSAGE,
        reply_markup=await main_kb()
    )

async def send_admin_answer(message: Message, **kwargs) -> None:
    parts = await parse_command_args(message, 3)
    _, client_id, source_message = parts
    
    asyncio.create_task(process_admin_answer(client_id, source_message))
    await message.answer("✅ Message successfully delivered")

async def set_ticket_status(message: Message, **kwargs) -> None:
    parts = await parse_command_args(message, 4)
    _, ticket_id, ticket_category, new_status = parts
    
    logger.info(f"Processing ticket status update: id={ticket_id}, category={ticket_category}, status={new_status}")
    
    # Ensure all parameters are strings
    ticket_id = str(ticket_id).strip()
    ticket_category = str(ticket_category).strip()
    new_status = str(new_status).strip()
    
    asyncio.create_task(
        process_ticket_status_update(ticket_id, new_status, ticket_category)
    )
    await message.answer("🔥 Ticket status has been successfully updated")

async def get_status(message: Message, **kwargs) -> None:
    parts = await parse_command_args(message, 3)
    _, ticket_id, ticket_category = parts
    
    # Ensure all parameters are strings
    ticket_id = str(ticket_id).strip()
    ticket_category = str(ticket_category).strip()
    
    logger.info(f"Getting ticket status: id={ticket_id}, category={ticket_category}")
    
    async for session in get_session():
        try:
            ticket_status = await get_ticket_status(ticket_id, ticket_category, session)
            response = (
                f"The current status of the ticket is: {ticket_status}\n\n"
                f"To change the status enter:\n"
                f"`/set_ticket_status | {ticket_id} | {ticket_category} | Ticket status`"
            )
            await message.answer(response, parse_mode="MarkdownV2")
            break
        except Exception as e:
            logger.error(f"Error in get_status: {e}")
            await send_log_to_dev()

async def get_tickets(message: Message, **kwargs) -> None:
    async for session in get_session():
        try:
            tickets = await get_all_tickets(session)
            
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
            break
        except Exception as e:
            logger.error(f"Error in get_tickets: {e}")
            await send_log_to_dev()

async def process_admin_answer(client_id: str, source_message: str) -> None:
    try:
        await send_photo_message(
            int(client_id),
            "src/resources/header_2.png",
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
    logger.info(f"Processing ticket status update in async task: id={ticket_id}, category={ticket_category}, status={new_status}")
    
    async for session in get_session():
        try:
            # Convert ticket_id to int and ensure category is string
            ticket_id_int = int(ticket_id)
            category_str = str(ticket_category)
            
            client_id = await get_user_id_by_message(session, ticket_id_int, category_str)
            if client_id is None:
                logger.error(f"Could not find client_id for ticket {ticket_id}")
                return
                
            await update_ticket_status(session, ticket_id_int, new_status, category_str)
            
            try:
                client_id_int = int(client_id)
                await send_photo_message(
                    client_id_int,
                    "src/resources/header_2.png",
                    f"🚀 The status of your ticket has been updated to:\n\n{new_status}"
                )
            except ValueError as e:
                logger.error(f"Invalid client_id format: {client_id}, error: {e}")
            break
        except Exception as err:
            logger.error(f"Error updating ticket status: {err}")
            await send_log_to_dev()

def register_admin_handlers(dp: Dispatcher) -> None:
    """Регистрация обработчиков команд администратора"""
    dp.message.register(error_handler(admin_required(send_admin_answer)), Command("admin_answer"))
    dp.message.register(error_handler(admin_required(set_ticket_status)), Command("set_ticket_status"))
    dp.message.register(error_handler(admin_required(get_status)), Command("get_ticket_status"))
    dp.message.register(error_handler(admin_required(get_tickets)), Command("get_all_tickets"))
    dp.message.register(error_handler(admin_required(get_help)), Command("help"))
