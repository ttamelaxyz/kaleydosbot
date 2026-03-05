# states.py
# ============================================
# Состояния FSM (Finite State Machine)
# ============================================

from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    """Состояния для регистрации пользователя"""
    name = State()
    age = State()
    phone = State()

class EventSelection(StatesGroup):
    """Состояния для подбора мероприятия"""
    budget = State()
    category = State()
    vibe = State()
    time = State()