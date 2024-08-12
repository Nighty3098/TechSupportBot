import asyncio

import requests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import types

from config import dp, logger, bot, CHANNEL
from send_logs import send_log_to_dev
from resources.TEXT_MESSAGES import DONE_TEXT
from db.check_for_qsl_injection import is_sql_injection_attempt

async def send_messages(message: types.Message, username: str, status: str):
    try:
        forward_text = ""
        channel_message = (
            f"🗒️ New report from @{username}\n"
            f"⚪ Category: {status}\n"
            f"🚀 To reply to a user enter the command: \n"
            f"`/admin_answer | {message.from_user.id} | your message`\n"
        )

        if message.text:
            forward_text += message.text
        
        if message.photo:
            photo = message.photo[-1]
            caption = message.caption if message.caption else "No description provided."
            channel_message += f"\n🔥 Report: {caption}"
            await bot.send_photo(chat_id=CHANNEL, photo=photo.file_id, caption=channel_message, parse_mode="Markdown")
        
        elif message.document:
            document = message.document
            caption = message.caption if message.caption else "No description provided."
            channel_message += f"\n🔥 Report: {caption}"
            await bot.send_document(chat_id=CHANNEL, document=document.file_id, caption=channel_message, parse_mode="Markdown")
        
        elif message.video:
            video = message.video
            caption = message.caption if message.caption else "No description provided."
            channel_message += f"\n🔥 Report: {caption}"
            await bot.send_video(chat_id=CHANNEL, video=video.file_id, caption=channel_message, parse_mode="Markdown")
        
        else:
            channel_message += f"\n🔥 Report: {forward_text}"
            await bot.send_message(chat_id=CHANNEL, text=channel_message, parse_mode="Markdown")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
