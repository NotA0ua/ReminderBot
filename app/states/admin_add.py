from aiogram.fsm.state import State, StatesGroup


class AdminAdd(StatesGroup):
    id = State()
    success = State()
