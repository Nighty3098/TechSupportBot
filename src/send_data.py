import asyncio

import requests
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import CHANNEL, NOTIFY_CHAT, bot, dp, logger
from db.check_for_qsl_injection import is_sql_injection_attempt
from db.db import create_connection, get_id_by_message
from resources.TEXT_MESSAGES import DONE_TEXT
from send_logs import send_log_to_dev

DEFAULT_CAPTION = "No description provided."


async def send_messages(message: types.Message, username: str, status: str, date: str):
    forward_text = ""
    channel_message = (
        f"🗒️ New report from @{username}\n"
        f"⚪ Category: {status}\n"
        f"🚀 To reply to a user enter the command: \n"
        f"/admin_answer | {message.from_user.id} | your message\n"
        f"🚀 To change the status of a ticket, enter the command: \n"
    )

    if message.text:
        forward_text += message.text
        message_id = await get_id_by_message(
            await create_connection(),
            forward_text,
            date,
            message.from_user.id,
            status.lower(),
        )
        channel_message += (
            f"/set_ticket_status | {message_id} | {status.lower()} | status\n"
        )

    if message.photo:
        photo = message.photo[-1]
        caption = message.caption if message.caption else DEFAULT_CAPTION
        message_id = await get_id_by_message(
            await create_connection(),
            caption,
            date,
            message.from_user.id,
            status.lower(),
        )
        channel_message += (
            f"/set_ticket_status | {message_id} | {status.lower()} | status\n"
        )
        channel_message += f"\n🔥 Report: \n\n{caption}"
        await bot.send_photo(
            chat_id=CHANNEL,
            photo=photo.file_id,
            caption=channel_message,
        )

    elif message.document:
        document = message.document
        caption = message.caption if message.caption else DEFAULT_CAPTION
        message_id = await get_id_by_message(
            await create_connection(),
            caption,
            date,
            message.from_user.id,
            status.lower(),
        )
        channel_message += (
            f"/set_ticket_status | {message_id} | {status.lower()} | status\n"
        )
        channel_message += f"\n🔥 Report: \n\n{caption}"
        await bot.send_document(
            chat_id=CHANNEL,
            document=document.file_id,
            caption=channel_message,
        )

    elif message.video:
        video = message.video
        caption = message.caption if message.caption else DEFAULT_CAPTION
        message_id = await get_id_by_message(
            await create_connection(),
            caption,
            date,
            message.from_user.id,
            status.lower(),
        )
        channel_message += (
            f"/set_ticket_status | {message_id} | {status.lower()} | status\n"
        )
        channel_message += f"\n🔥 Report: \n\n{caption}"
        await bot.send_video(
            chat_id=CHANNEL,
            video=video.file_id,
            caption=channel_message,
        )

    else:
        channel_message += f"\n🔥 Report: \n\n{forward_text}"
        await bot.send_message(chat_id=CHANNEL, text=channel_message)
