from aiogram.fsm.state import StatesGroup, State


class UserRegistration(StatesGroup):
    phone = State()
    full_name = State()
