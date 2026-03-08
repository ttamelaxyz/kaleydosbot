from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):

    name = State()
    gender = State()
    phone = State()


class Search(StatesGroup):

    budget = State()
    place = State()
    atmosphere = State()
    time = State()


class AddEvent(StatesGroup):

    name = State()
    description = State()
    place = State()
    atmosphere = State()
    time = State()
    budget = State()
    link = State()
    image = State()