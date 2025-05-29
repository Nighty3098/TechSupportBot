import asyncio
import datetime
import re
from typing import Optional

from aiogram import types
from aiogram.types import Message

from config import CHANNEL, bot, logger
from db.crud import get_id_by_message
from db.database import get_session
from send_logs import send_log_to_dev


def escape_markdown(text: str) -> str:
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


async def send_messages(
    message: Message,
    username: str,
    report_type: str,
    responsdate: str,
) -> None:
    try:
        message_text = message.text or message.caption or 'No description provided.'
        escaped_message = escape_markdown(message_text)
        escaped_username = escape_markdown(username)
        escaped_date = escape_markdown(responsdate)
        escaped_user_id = escape_markdown(str(message.from_user.id))
        escaped_report_type = escape_markdown(report_type.lower())

        channel_message = (
            f"🚨 New {escaped_report_type} from @{escaped_username}\n\n"
            f"📝 Message: {escaped_message}\n"
            f"⏰ Date: {escaped_date}\n"
            f"🆔 User ID: {escaped_user_id}"
        )

        await bot.send_message(
            chat_id=CHANNEL,
            text=channel_message,
            parse_mode="MarkdownV2",
        )

        async for session in get_session():
            message_id = await get_id_by_message(
                session=session,
                message_value=message_text,
                date=datetime.datetime.strptime(responsdate, "%d-%m-%Y %H:%M:%S"),
                user_id=str(message.from_user.id),
                category=report_type.lower(),
            )

        if message_id:
            logger.info(f"Message ID: {message_id}")
        else:
            logger.warning("Message ID not found")

    except Exception as err:
        logger.error(f"Error in send_messages: {err}", exc_info=True)
        await send_log_to_dev()
