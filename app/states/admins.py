from aiogram.fsm.state import State, StatesGroup


class Admins(StatesGroup):
    admin_add = State()
    admin_id = State()
