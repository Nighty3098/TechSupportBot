import asyncio

from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.filters import callback_data
from aiogram.types import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import *
from requests.models import *

from config import *

async def main_kb():
    try:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="🔴 Bug report 🔴", callback_data="BugReport"))
        builder.add(types.InlineKeyboardButton(text="🚀 Suggest an idea 🚀", callback_data="SuggestIdea"))
        builder.add(types.InlineKeyboardButton(text="💬 Contacts 💬", callback_data="Contacts"))
        builder.add(types.InlineKeyboardButton(text="📁 Our products 📁", callback_data="OurProducts"))

        builder.adjust(2)

        logger.debug("Creating user panel")

        return builder.as_markup()
    except Exception as err:
        logger.error(f"{err}")

async def back_btn():
    try:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="🔙 Back", callback_data="Back"))
        builder.adjust(1)

        logger.debug("Creating back button")

        return builder.as_markup()
    except Exception as err:
        logger.error(f"{err}")
