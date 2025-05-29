import logging

from aiogram import Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from config import NOTIFY_CHAT, bot, logger
from db.database import get_session
from kb_builder import main_kb
from resources.TEXT_MESSAGES import HELLO_MESSAGE
from send_logs import send_log_to_dev
from client import (
    back_to_menu,
    contacts,
    get_users_bug,
    get_users_idea,
    our_products,
    support_me,
    user_message_bug,
    user_message_idea,
)
from StatesGroup import GetBug, GetIdea


async def main_menu(message: Message) -> None:
    try:
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        member = await bot.get_chat_member(chat_id, user_id)
        username = member.user.username

        await message.answer_photo(
            photo=FSInputFile("resources/header_2.png"),
            caption=HELLO_MESSAGE,
            reply_markup=await main_kb(),
            parse_mode="MarkdownV2",
        )

        logger.info(f"{user_id} - main menu")

        message_for_dev = f"New user: @{username}"
        await bot.send_message(chat_id=NOTIFY_CHAT, text=message_for_dev)

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


def register_handlers(dp: Dispatcher) -> None:
    """Регистрация всех обработчиков"""
    # Обработчик команды /start
    dp.message.register(main_menu, CommandStart())
    
    # Обработчики callback-запросов
    dp.callback_query.register(get_users_idea, F.data == "SuggestIdea")
    dp.callback_query.register(get_users_bug, F.data == "BugReport")
    dp.callback_query.register(back_to_menu, F.data == "Back")
    dp.callback_query.register(contacts, F.data == "Contacts")
    dp.callback_query.register(our_products, F.data == "OurProducts")
    dp.callback_query.register(support_me, F.data == "SupportMe")

    # Обработчики сообщений
    dp.message.register(user_message_idea, GetIdea.wait_for_message)
    dp.message.register(user_message_bug, GetBug.wait_for_message)
