from aiogram import types
from aiogram.types import FSInputFile

from config import dp, bot, CHANNEL, logger
from send_logs import send_log_to_dev

async def get_users() -> list[int]:
    """
    Gets a list of channel administrators' IDs.
    
    Returns:
        list[int]: A list of administrator IDs. In case of an error, it returns an empty list.
    """
    try:
        admins = await bot.get_chat_administrators(CHANNEL)
        return [admin.user.id for admin in admins]
    except Exception as err:
        logger.error(f"Error fetching admins: {err}", exc_info=True)
        await send_log_to_dev()
        return []
