import asyncio
import requests

from StatesGroup import *

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from send_logs import *
from config import *

async def send_messages(user_message, state: FSMContext, username, status) -> None:
    try:
        for dev in DEVS:
            try:
                if status == "Bug": 
                    content_status = "🔴 BUG 🔴\n"
                if status == "Idea":
                    content_status = "🍀 IDEA 🍀\n"
                else :
                    content_status = ""


                logger.debug(dev)
                edited_user_message = content_status + "\n @" + username + "\n" + user_message
                await bot.send_message(dev, edited_user_message, allow_sending_without_reply=True)
            except Exception as e:
                await send_log_to_dev()
                logger.error(f"dev:{dev} Error: {e}")
    except Exception as e:
        await send_log_to_dev()
        logger.error(f"Error: {e}")


async def send_messages_with_picture(file_id, caption, state: FSMContext, username, status) -> None:
    try:       
        for dev in DEVS:
            try:
                if status == "Bug": 
                    content_status = "🔴 BUG 🔴\n"
                if status == "Idea":
                    content_status = "🍀 IDEA 🍀\n"
                else :
                    content_status = ""


                logger.debug(dev)
                edited_user_message = "@" + username + "\n" + caption
                await bot.send_photo(dev, photo=file_id, caption=edited_user_message, allow_sending_without_reply=True)
            except Exception as e:
                await send_log_to_dev()
                logger.error(f"dev:{dev} Error: {e}")
    except Exception as e:
        await send_log_to_dev()
        logger.error(f"Error: {e}")