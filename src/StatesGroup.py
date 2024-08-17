from aiogram.fsm.state import State, StatesGroup

class GetIdea(StatesGroup):
    none_state = State()
    wait_for_message = State()
    done = State()

class GetBug(StatesGroup):
    none_state = State()
    wait_for_message = State()
    done = State()
