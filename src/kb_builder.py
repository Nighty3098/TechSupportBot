import asyncio

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


from config import log_file, data, DEVS, CHANNEL, bot, dp, logger

async def main_kb():
    try:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="🔴 Bug report 🔴", callback_data="BugReport"))
        builder.add(types.InlineKeyboardButton(text="🚀 Suggest an idea 🚀", callback_data="SuggestIdea"))
        builder.add(types.InlineKeyboardButton(text="💬 Contacts 💬", callback_data="Contacts"))
        builder.add(types.InlineKeyboardButton(text="📁 Our products 📁", callback_data="OurProducts"))
        builder.add(types.InlineKeyboardButton(text="🏦 Support Me 🏦", callback_data="SupportMe"))

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
