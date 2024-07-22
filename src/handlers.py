import asyncio
import json
import logging

from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.filters import callback_data
from aiogram.types import *
from aiogram.types import message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import *
from aiogram.types.input_media_photo import *
from aiogram.types import input_media_photo

from config import *
from resources.TEXT_MESSAGES import *
from send_logs import *
from kb_builder import *
from send_data import *
from StatesGroup import *

@dp.message(CommandStart())
async def main_menu(message: Message) -> None:
    try:
        global user_id, message_id
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        member = await bot.get_chat_member(chat_id, user_id)
        username = member.user.username

        image_path = 'resources/TechSupport.png'

        photo = FSInputFile(image_path)
        message_id = await message.answer_photo(photo, caption=HELLO_MESSAGE, reply_markup=await main_kb())

        logger.debug(f"{user_id} - main menu")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "SuggestIdea")
async def GetUserIdea(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(GetIdea.wait_for_message)

        logger.debug(f"{callback.message.chat.id} - idea suggest")

        message_id = callback.message.message_id

        await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=message_id, caption=IDEA_TEXT, reply_markup=await back_btn())

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "BugReport")
async def GetUserBug(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(GetBug.wait_for_message)

        logger.debug(f"{callback.message.chat.id} - bug report")

        message_id = callback.message.message_id

        await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=message_id, caption=BUG_TEXT, reply_markup=await back_btn())

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.message(GetIdea.wait_for_message)
async def IdeaUserMessage(message: Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.debug(f"Idea suggest from {username}: {message.text}")

        try:
            await send_messages(message, username, "🍀 IDEA 🍀")
        except Exception as e:
            logging.error(f"Error forwarding message from {username} to {CHANNEL}: {e}")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetBug.wait_for_message)
async def BugUserMessage(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.debug(f"Bug report from {username}: {message.text}")

        try:
            await send_messages(message, username, "❌ BUG ❌")
        except Exception as e:
            logging.error(f"Error forwarding message from {username} to {CHANNEL}: {e}")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "Back")
async def BackToStartMenu(callback: types.CallbackQuery):
    try:
        logger.debug(f"{callback.message.chat.id} - back button")

        message_id = callback.message.message_id

        await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=message_id, caption=HELLO_MESSAGE, reply_markup=await main_kb())

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "Contacts")
async def Contacts(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - contacts")

        await callback.message.answer(DEVS_TEXT, reply_markup=await back_btn(), disable_web_page_preview=True)
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.callback_query(F.data == "OurProducts")
async def OurProducts(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - our products")

        message_id = callback.message.message_id

        await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=message_id, caption=OUR_PRODUCTS_TEXT, reply_markup=await back_btn())

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "SupportMe")
async def SupportMe(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - support me")

        await callback.message.answer(SUPPORT_TEXT, reply_markup=await back_btn())
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
