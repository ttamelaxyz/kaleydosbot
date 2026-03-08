from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():

    keyboard = [
        [KeyboardButton(text="🎯 Подобрать мероприятие")],
        [KeyboardButton(text="🏙 События недели")],
        [KeyboardButton(text="🎲 Случайное событие")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def places():

    keyboard = [
        [KeyboardButton(text="Кино")],
        [KeyboardButton(text="Концерт")],
        [KeyboardButton(text="Выставка")],
        [KeyboardButton(text="Мастер-класс")],
        [KeyboardButton(text="Вечеринка")],
        [KeyboardButton(text="Театры и стендапы")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def atmosphere():

    keyboard = [
        [KeyboardButton(text="Спокойная")],
        [KeyboardButton(text="Активная")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def time():

    keyboard = [
        [KeyboardButton(text="День")],
        [KeyboardButton(text="Вечер")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def event_buttons():

    keyboard = [
        [KeyboardButton(text="🔁 Другое мероприятие")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)