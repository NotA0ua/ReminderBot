from aiogram.fsm.state import State, StatesGroup


class AdminAdd(StatesGroup):
    admin_add = State()
    admin_id = State()
