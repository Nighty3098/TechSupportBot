import asyncio
import requests

from StatesGroup import *

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from send_logs import *
from config import *

async def send_messages(message, username, status):
    try:
        await bot.send_message(CHANNEL, f"\n\n{status}\n\nReport from @{username}\n\n")
        await message.forward(CHANNEL)
    
    except Exception as e:
        await send_log_to_dev()
        logger.error(f"Error: {e}")
