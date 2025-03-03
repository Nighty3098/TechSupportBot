import logging
from aiogram.types import FSInputFile
from aiogram.enums.chat_action import ChatAction

from config import bot, logger, log_file, NOTIFY_CHAT

async def send_log_to_dev() -> None:
    """
    Sends the log file to the developer in the specified chat.

    The logs are sent as a document with a prior notification of the action (document upload).
    In case of an error, an exception is logged.
    """
    try:
        log_file_input = FSInputFile(log_file, filename="TechSupport.log")
        
        await bot.send_chat_action(chat_id=NOTIFY_CHAT, action=ChatAction.UPLOAD_DOCUMENT)
        
        await bot.send_document(
            chat_id=NOTIFY_CHAT,
            document=log_file_input,
            allow_sending_without_reply=True
        )
        
        logger.warning(f"Logs sent to dev chat: {NOTIFY_CHAT}")
    except Exception as err:
        logger.error(f"Failed to send logs: {err}", exc_info=True)
