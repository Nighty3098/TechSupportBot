from aiogram import F, handlers, types
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.types.input_file import InputFile

from config import dp, bot, CHANNEL, logger
from send_logs import send_log_to_dev

async def get_users():
    try:
        admins = await bot.get_chat_administrators(CHANNEL)
        admin_ids = [admin.user.id for admin in admins]
        
        return admin_ids
    except Exception as err:
        return ""
        logger.error(f"{err}")
        await send_log_to_dev()
