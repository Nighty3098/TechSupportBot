import asyncio

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL, DEVS, bot, data, dp, log_file, logger


async def main_kb():
    try:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="🔴 Bug report 🔴", callback_data="BugReport"
            )
        )
        builder.add(
            types.InlineKeyboardButton(
                text="💫 Suggest an idea 💫", callback_data="SuggestIdea"
            )
        )
        builder.add(
            types.InlineKeyboardButton(text="💬 Contacts 💬", callback_data="Contacts")
        )
        builder.add(
            types.InlineKeyboardButton(
                text="🏦 Support Me 🏦", callback_data="SupportMe"
            )
        )
        builder.add(
            types.InlineKeyboardButton(
                text="🛠️ Order programme development 🛠️", url="https://t.me/night3098"
            )
        )

        builder.adjust(2)

        logger.debug("Creating user panel")

        return builder.as_markup()
    except Exception as err:
        logger.error(f"{err}")


async def back_btn():
    try:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="⮜ Back", callback_data="Back"))
        builder.adjust(1)

        logger.debug("Creating back button")

        return builder.as_markup()
    except Exception as err:
        logger.error(f"{err}")


async def contacts_btn():
    try:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="⭐ Discord server", url="https://discord.gg/tnHSEc2cZv"
            )
        )
        builder.add(
            types.InlineKeyboardButton(
                text="⭐ Discord", url="https://discord.gg/#9707"
            )
        )
        builder.add(
            types.InlineKeyboardButton(text="⭐ Telegram", url="https://t.me/night3098")
        )
        builder.add(
            types.InlineKeyboardButton(
                text="⭐ Reddit", url="https://www.reddit.com/user/DEVELOPER0x31/"
            )
        )
        builder.add(
            types.InlineKeyboardButton(
                text="⭐ Dev.to", url="https://dev.to/nighty3098"
            )
        )
        builder.add(types.InlineKeyboardButton(text="⮜ Back", callback_data="Back"))
        builder.adjust(2)

        logger.debug("Creating contacts button")

        return builder.as_markup()
    except Exception as err:
        logger.error(f"{err}")
