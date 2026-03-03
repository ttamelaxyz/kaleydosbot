from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_contact_keyboard():
    """Клавиатура для отправки контакта"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_gender_keyboard():
    """Клавиатура для выбора пола"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨 Мужской"), KeyboardButton(text="👩 Женский")],
            [KeyboardButton(text="⚪ Другое")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_city_keyboard():
    """Клавиатура для выбора города"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Москва"), KeyboardButton(text="Санкт-Петербург")],
            [KeyboardButton(text="Казань"), KeyboardButton(text="Другой город")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_event_type_keyboard():
    """Клавиатура для выбора типа события"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Кино")],
            [KeyboardButton(text="🎵 Концерт")],
            [KeyboardButton(text="🎨 Выставка")],
            [KeyboardButton(text="🎭 Театр")],
            [KeyboardButton(text="🎮 Квиз/Антикафе")],
            [KeyboardButton(text="❓ Не важно")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_company_keyboard():
    """Клавиатура для выбора компании"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Иду один/одна")],
            [KeyboardButton(text="💑 Иду с парой/второй половинкой")],
            [KeyboardButton(text="👥 Иду с друзьями")],
            [KeyboardButton(text="❓ Не важно")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_main_menu():
    """Главное меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Подобрать событие")],
            [KeyboardButton(text="📍 Сменить город")],
            [KeyboardButton(text="📋 Мои данные")]
        ],
        resize_keyboard=True
    )
    return keyboard