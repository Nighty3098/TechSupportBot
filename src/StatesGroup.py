from aiogram import *
from aiogram.fsm.state import State, StatesGroup

class GetIdea(StatesGroup):
    wait_for_message = State()

class GetBug(StatesGroup):
    wait_for_message = State()
