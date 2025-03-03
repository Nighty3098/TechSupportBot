import asyncio
from typing import Optional, Dict, Any

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import CHANNEL, NOTIFY_CHAT, bot, dp, logger
from db.check_for_qsl_injection import is_sql_injection_attempt
from db.db import create_connection, get_id_by_message
from resources.TEXT_MESSAGES import DONE_TEXT
from send_logs import send_log_to_dev

DEFAULT_CAPTION = "No description provided."

MEDIA_TYPES = {
    "photo": {"method": bot.send_photo, "field": "photo"},
    "document": {"method": bot.send_document, "field": "document"},
    "video": {"method": bot.send_video, "field": "video"},
}

async def send_messages(message: types.Message, username: str, status: str, date: str) -> None:
    """
    Sends the user's report to the channel with the appropriate formatting and status tracking.

    Args:
        message (types.Message): A message from the user.
        username (user): The user's name.
        status (str): The status of the report.
        date (str): The date when the report was created.
    """
    status_lower = status.lower()
    channel_message = (
        f"🗒️ New report from @{username}\n"
        f"⚪ Category: {status}\n\n"
        f"🚀 To reply to user:\n/admin_answer | {message.from_user.id} | your message\n"
        f"🚀 To change ticket status:\n/set_ticket_status | [ID] | {status_lower} | status\n"
    )

    content, media_object, media_type = await _extract_message_content(message)
    if not content:
        logger.warning(f"Unsupported message type from {username}")
        return

    async with create_connection() as conn:
        try:
            message_id = await get_id_by_message(
                conn, content, date, message.from_user.id, status_lower
            )
            if not message_id:
                logger.error(f"Failed to get ID for {media_type} message from {username}")
                return

            channel_message = channel_message.replace("[ID]", str(message_id))
            channel_message += f"\n🔥 Report: \n\n{content}"

            await _send_to_channel(media_type, media_object, channel_message, username)
        except Exception as e:
            logger.critical(f"Error processing {media_type} message: {str(e)}", exc_info=True)
            await send_log_to_dev()

async def _extract_message_content(message: types.Message) -> tuple[str, Optional[Any], str]:
    """
    Extracts the content and media type from the message.

    Args:
        message (types.Message): A message from the user.

    Returns:
        tuple[std, Optional[Any], str]: Content, media object, and media type.
    """
    if message.text:
        return message.text, None, "text"
    elif message.photo:
        return message.caption or DEFAULT_CAPTION, message.photo[-1], "photo"
    elif message.document:
        return message.caption or DEFAULT_CAPTION, message.document, "document"
    elif message.video:
        return message.caption or DEFAULT_CAPTION, message.video, "video"
    return "", None, "unknown"

async def _send_to_channel(
    media_type: str, media_object: Optional[Any], channel_message: str, username: str
) -> None:
    """
    Sends a message to the channel depending on the type of media.

    Args:
        media_type (str): Media type (text, photo, document, video).
        media_object (Optional[Any]): A media object (if any).
        channel_message (str): The text of the message.
        username (user): The user's name.
    """
    if media_type == "text":
        await bot.send_message(chat_id=CHANNEL, text=channel_message)
        logger.info(f"Text message sent to channel for user {username}")
    else:
        method_info = MEDIA_TYPES.get(media_type)
        if not method_info:
            logger.warning(f"Unsupported media type: {media_type}")
            return

        await method_info["method"](
            chat_id=CHANNEL,
            **{method_info["field"]: media_object.file_id},
            caption=channel_message,
        )
        logger.info(f"{media_type.capitalize()} message sent to channel for user {username}")
