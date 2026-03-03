from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    """Состояния для регистрации пользователя"""
    name = State()
    gender = State()
    phone = State()
    city = State()

class EventSelection(StatesGroup):
    """Состояния для выбора событий"""
    event_type = State()
    company = State()