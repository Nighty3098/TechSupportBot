import asyncio
import logging

from aiogram import F, handlers, types
from aiogram.filters import Command, CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_chat_action import SendChatAction
from aiogram.types import FSInputFile, Message
from aiogram.types.input_file import InputFile

from config import CHANNEL, DEVS, TOKEN, bot, data, dp, log_file, logger
from db.db import (create_connection, create_table, get_all_tickets,
                   get_ticket_status, get_user_id_by_message, save_report_data,
                   update_ticket_status)
from get_admins_id import get_users
from kb_builder import back_btn, main_kb
from resources.TEXT_MESSAGES import (BUG_TEXT, DEVS_TEXT, DONE_TEXT,
                                     HELLO_MESSAGE, IDEA_TEXT,
                                     INCORRECT_INPUT_FORMAT_ERROR,
                                     OUR_PRODUCTS_TEXT, SUPPORT_TEXT, HELP_MESSAGE)
from send_data import send_messages
from send_logs import send_log_to_dev
from StatesGroup import GetBug, GetIdea
async def process_admin_answer(client_id, source_message):
    try:
        image_path = "resources/header_2.png"
        photo = FSInputFile(image_path)

        admin_message_text = f"🔥 Message from admin:\n\n{source_message}"
        logger.debug(await bot.send_photo(
            photo=photo,
            chat_id=client_id,
            caption=admin_message_text,
        ))
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


async def process_ticket_status_update(ticket_id, new_status, ticket_category):
    try:
        image_path = "resources/header_2.png"
        photo = FSInputFile(image_path)

        client_id = await get_user_id_by_message(
            await create_connection(), ticket_id, ticket_category
        )
        await update_ticket_status(
            await create_connection(), ticket_id, new_status, ticket_category
        )
        logger.debug(await bot.send_photo(
            photo=photo,
            chat_id=client_id,
            caption=f"🚀 The status of your ticket has been updated to:\n\n{new_status}",
        ))
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(Command("admin_answer"))
async def send_admin_answer(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(
                f"User {message.from_user.username} : {user_id} trying to exec admin_answer command"
            )
        else:
            logger.warning(
                f"User: {message.from_user.username} : {user_id} - admin_answer"
            )

            parts = message.text.split(" | ")

            if len(parts) != 3:
                logger.error(INCORRECT_INPUT_FORMAT_ERROR)
            else:
                client_id = parts[1]
                source_message = parts[2]

                asyncio.create_task(process_admin_answer(client_id, source_message))

                logger.debug(await message.answer(
                    "✅ Message successfully delivered"
                ))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(Command("set_ticket_status"))
async def set_ticket_status(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(
                f"User {message.from_user.username} : {user_id} trying to exec set_ticket_status command"
            )
        else:
            logger.warning(
                f"User: {message.from_user.username} : {user_id} - set_ticket_status"
            )

            parts = message.text.split(" | ")

            if len(parts) != 4:
                logger.error("Incorrect input format")
            else:
                ticket_id = parts[1]
                ticket_category = parts[2]
                new_status = parts[3]

                asyncio.create_task(
                    process_ticket_status_update(ticket_id, new_status, ticket_category)
                )
                logger.debug(await message.answer(
                    "🔥 Ticket status has been successfully updated",
                ))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(Command("get_ticket_status"))
async def get_status(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(
                f"User {message.from_user.username} : {user_id} trying to exec get_ticket_status command"
            )
        else:
            logger.warning(
                f"User: {message.from_user.username} : {user_id} - get_ticket_status"
            )

            parts = message.text.split(" | ")

            if len(parts) != 3:
                logger.error("Incorrect input format")
            else:
                ticket_id = parts[1]
                ticket_category = parts[2]

                ticket_status = await get_ticket_status(
                    await create_connection(), ticket_id, ticket_category
                )

                logger.debug(await message.answer(
                    f"The current status of the ticket is\\: {ticket_status}\n\nTo change the status enter\\:\n`\\/set_ticket_status \\| {ticket_id} \\| {ticket_category.lower()} \\| Ticket status`", parse_mode="MarkdownV2"
                ))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(Command("get_all_tickets"))
async def get_tickets(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(
                f"User {message.from_user.username} : {user_id} trying to exec get_all_tickets command"
            )
        else:
            logger.warning(
                f"User: {message.from_user.username} : {user_id} - get_all_tickets"
            )

            ticket_messages = []
            tickets = await get_all_tickets(await create_connection())
            for ticket in tickets:
                ticket_messages.append(
                    f"ID: {ticket['id']}\nCategory: {ticket['category']}\nStatus: {ticket['status']}\nUser ID: {ticket['user_id']}\nUsername: @{ticket['username']}\nMessage:\n{ticket['message']}"
                )
            full_message = "\n\n".join(ticket_messages)

            with open("AllTickets.txt", "w", encoding="utf-8") as f:
                f.write(full_message)

            if not full_message:
                logger.debug(await message.answer("No data available"))
            else:
                logger.debug(await bot.send_chat_action(action="upload_document", chat_id=user_id))
                logger.debug(await message.answer_document(FSInputFile("AllTickets.txt"), caption="👾 *_All tickets_* 👾", parse_mode="MarkdownV2"))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(Command("get_db"))
async def get_db(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(
                f"User {message.from_user.username} : {user_id} trying to exec get_db command"
            )
        else:
            logger.warning(f"User: {message.from_user.username} : {user_id} - get_db")

            try:
                await bot.send_chat_action(action="upload_document", chat_id=user_id)
                with open(data, "rb") as db_file:
                    logger.debug(await message.answer_document(FSInputFile(data), caption="👾 DXS GROUP DB 👾"))
            except FileNotFoundError:
                logger.debug(await message.answer("DB File not found."))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.message(Command("help"))
async def get_db(message: Message):
    try:
        user_id = message.from_user.id
        admins = await get_users()
        logger.debug(f"Loading admins list: {admins}")

        if user_id not in admins:
            logger.warning(
                f"User {message.from_user.username} : {user_id} trying to exec help command"
            )
        else:
            image_path = "resources/header_2.png"

            logger.warning(f"User: {message.from_user.username} : {user_id} - help")
            logger.debug(await message.answer_photo(photo=FSInputFile(image_path), caption=HELP_MESSAGE, parse_mode="MarkdownV2"))

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
