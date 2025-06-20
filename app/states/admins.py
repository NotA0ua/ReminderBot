from aiogram.fsm.state import State, StatesGroup


class Admins(StatesGroup):
    admins = State()
    admin = State()
