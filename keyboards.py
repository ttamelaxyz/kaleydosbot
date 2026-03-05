# keyboards.py
# ============================================
# Все клавиатуры бота
# ============================================

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import CATEGORIES, VIBE_MAP, TIME_MAP

def get_contact_keyboard():
    """Клавиатура для отправки номера телефона"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📱 Отправить номер", request_contact=True))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_main_menu_keyboard():
    """Главное меню после регистрации"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🎯 Подобрать мероприятие"))
    builder.add(KeyboardButton(text="📅 События в городе"))
    builder.add(KeyboardButton(text="🎲 Не хочу думать"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_event_actions_keyboard(event_url: str):
    """Инлайн клавиатура под предложенным мероприятием"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔄 Другое мероприятие", callback_data="another_event"))
    builder.add(InlineKeyboardButton(text="🔗 Ссылка на мероприятие", url=event_url))
    builder.add(InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def get_categories_keyboard():
    """Клавиатура с категориями для подбора"""
    builder = ReplyKeyboardBuilder()
    for cat in CATEGORIES:
        builder.add(KeyboardButton(text=cat))
    builder.add(KeyboardButton(text="🏠 Главное меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_vibe_keyboard():
    """Клавиатура для выбора атмосферы"""
    builder = ReplyKeyboardBuilder()
    for vibe in VIBE_MAP.keys():
        builder.add(KeyboardButton(text=vibe))
    builder.add(KeyboardButton(text="🏠 Главное меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_time_keyboard():
    """Клавиатура для выбора времени"""
    builder = ReplyKeyboardBuilder()
    for time in TIME_MAP.keys():
        builder.add(KeyboardButton(text=time))
    builder.add(KeyboardButton(text="🏠 Главное меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_back_to_menu_keyboard():
    """Клавиатура с одной кнопкой возврата в меню"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🏠 Главное меню"))
    return builder.as_markup(resize_keyboard=True)