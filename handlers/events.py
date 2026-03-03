from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.reply import (
    get_event_type_keyboard, 
    get_company_keyboard,
    get_main_menu
)
from utils.states import EventSelection
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardRemove
import database

router = Router()

# Словарь для преобразования текста кнопок в типы событий
EVENT_TYPE_MAP = {
    "🎬 Кино": "кино",
    "🎵 Концерт": "концерт",
    "🎨 Выставка": "выставка",
    "🎭 Театр": "театр",
    "🎮 Квиз/Антикафе": "квиз"
}

# Словарь для преобразования текста кнопок в типы компании
COMPANY_MAP = {
    "👤 Иду один/одна": "один",
    "💑 Иду с парой/второй половинкой": "пара",
    "👥 Иду с друзьями": "друзья"
}

@router.message(F.text == "🎯 Подобрать событие")
async def cmd_find_events(message: types.Message, state: FSMContext):
    """Начать подбор событий"""
    user_id = message.from_user.id
    user = database.get_user(user_id)
    
    if not user:
        await message.answer(
            "Сначала нужно зарегистрироваться! Напишите /start"
        )
        return
    
    await message.answer(
        f"Ищем события в городе {user['city']}! 🎉\n"
        "Какой тип мероприятий вас интересует?",
        reply_markup=get_event_type_keyboard()
    )
    await state.set_state(EventSelection.event_type)

@router.message(EventSelection.event_type)
async def process_event_type(message: types.Message, state: FSMContext):
    """Обработка выбора типа события"""
    if message.text == "❓ Не важно":
        event_type = None
    elif message.text in EVENT_TYPE_MAP:
        event_type = EVENT_TYPE_MAP[message.text]
    else:
        await message.answer(
            "Пожалуйста, выберите тип события из предложенных вариантов:",
            reply_markup=get_event_type_keyboard()
        )
        return
    
    await state.update_data(event_type=event_type)
    await message.answer(
        "С кем планируете пойти?",
        reply_markup=get_company_keyboard()
    )
    await state.set_state(EventSelection.company)

@router.message(EventSelection.company)
async def process_company(message: types.Message, state: FSMContext):
    """Обработка выбора компании и показ результатов"""
    if message.text == "❓ Не важно":
        company = None
    elif message.text in COMPANY_MAP:
        company = COMPANY_MAP[message.text]
    else:
        await message.answer(
            "Пожалуйста, выберите вариант из предложенных:",
            reply_markup=get_company_keyboard()
        )
        return
    
    # Получаем данные пользователя
    user_data = await state.get_data()
    user_id = message.from_user.id
    user = database.get_user(user_id)
    
    # Ищем подходящие события
    events = database.get_events_by_preferences(
        city=user['city'],
        event_type=user_data.get('event_type'),
        company=company
    )
    
    if not events:
        await message.answer(
            f"😔 К сожалению, в городе {user['city']} не нашлось событий по вашим критериям.\n"
            "Попробуйте изменить параметры поиска!",
            reply_markup=get_main_menu()
        )
        await state.clear()
        return
    
    # Отправляем результаты
    await message.answer(
        f"✨ Нашлось {len(events)} событий! ✨\n",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Отправляем каждое событие отдельным сообщением
    for event in events:
        event_text = (
            f"🎯 <b>{event['title']}</b>\n"
            f"📍 Тип: {event['type'].capitalize()}\n"
            f"📝 {event['description']}\n"
        )
        
        if company:
            event_text += f"👥 Рекомендуется для: {company}"
        
        await message.answer(event_text, parse_mode="HTML")
    
    await message.answer(
        "Хотите подобрать еще события?",
        reply_markup=get_main_menu()
    )
    
    await state.clear()

@router.message(F.text == "📍 Сменить город")
async def cmd_change_city(message: types.Message, state: FSMContext):
    """Смена города"""
    await message.answer(
        "Введите ваш новый город:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state("changing_city")

@router.message(F.text == "📋 Мои данные")
async def cmd_show_profile(message: types.Message):
    """Показать данные пользователя"""
    user_id = message.from_user.id
    user = database.get_user(user_id)
    
    if user:
        gender_text = {
            "male": "👨 Мужской",
            "female": "👩 Женский",
            "other": "⚪ Другое"
        }.get(user['gender'], "Не указан")
        
        profile_text = (
            "📋 <b>Ваш профиль:</b>\n\n"
            f"👤 Имя: {user['name']}\n"
            f"⚪ Пол: {gender_text}\n"
            f"📱 Телефон: {user['phone']}\n"
            f"📍 Город: {user['city']}"
        )
        
        await message.answer(profile_text, parse_mode="HTML")
    else:
        await message.answer(
            "Вы еще не зарегистрированы. Напишите /start"
        )

@router.message(StateFilter("changing_city"))
async def process_city_change(message: types.Message, state: FSMContext):
    """Обработка смены города"""
    new_city = message.text.strip()
    user_id = message.from_user.id
    user = database.get_user(user_id)
    
    if user:
        user['city'] = new_city
        database.save_user(user_id, user)
        
        await message.answer(
            f"Город успешно изменен на {new_city}! ✅",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer(
            "Произошла ошибка. Попробуйте перезапустить бота командой /start"
        )
    
    await state.clear()