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
    """Send user report to channel with appropriate formatting and status tracking."""
    status_lower = status.lower()
    channel_message = (
        f"🗒️ New report from @{username}\n"
        f"⚪ Category: {status}\n\n"
        f"🚀 To reply to user:\n/admin_answer | {message.from_user.id} | your message\n"
        f"🚀 To change ticket status:\n/set_ticket_status | [ID] | {status_lower} | status\n"
    )

    content = ""
    media_object = None
    media_type = "text"

    with await create_connection() as conn:
        try:
            if message.text:
                content = message.text
                media_type = "text"
            elif message.photo:
                media_object = message.photo[-1]
                content = message.caption or DEFAULT_CAPTION
                media_type = "photo"
            elif message.document:
                media_object = message.document
                content = message.caption or DEFAULT_CAPTION
                media_type = "document"
            elif message.video:
                media_object = message.video
                content = message.caption or DEFAULT_CAPTION
                media_type = "video"
            else:
                logger.warning(f"Unsupported message type from {username}")
                return

            message_id = await get_id_by_message(
                conn, content, date, message.from_user.id, status_lower
            )

            logger.debug(f"Retrieved message ID: {message_id} for {media_type} content")

            if not message_id:
                logger.error(
                    f"Failed to get ID for {media_type} message from {username}"
                )
                return

            channel_message = channel_message.replace("[ID]", str(message_id))
            channel_message += f"\n🔥 Report: \n\n{content}"

            if media_type == "text":
                await bot.send_message(chat_id=CHANNEL, text=channel_message)
                logger.info(f"Text message sent to channel for user {username}")
            else:
                send_method = {
                    "photo": bot.send_photo,
                    "document": bot.send_document,
                    "video": bot.send_video,
                }[media_type]

                await send_method(
                    chat_id=CHANNEL,
                    **{media_type: media_object.file_id},
                    caption=channel_message,
                )
                logger.info(
                    f"{media_type.capitalize()} message sent to channel for user {username}"
                )

        except Exception as e:
            logger.critical(
                f"Error processing {media_type} message: {str(e)}", exc_info=True
            )
            await send_log_to_dev()
