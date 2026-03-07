from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    name = State()
    age = State()
    phone = State()

class EventSearch(StatesGroup):
    budget = State()
    place = State()
    atmosphere = State()
    time = State()