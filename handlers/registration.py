from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.reply import (
    get_gender_keyboard, 
    get_contact_keyboard, 
    get_city_keyboard,
    get_main_menu
)
from utils.states import Registration
import database

router = Router()

@router.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    """Обработка имени пользователя"""
    name = message.text.strip()
    
    # Простая валидация имени
    if len(name) < 2 or len(name) > 50:
        await message.answer("Пожалуйста, введите корректное имя (от 2 до 50 символов):")
        return
    
    await state.update_data(name=name)
    await message.answer(
        f"Приятно познакомиться, {name}! Выберите ваш пол:",
        reply_markup=get_gender_keyboard()
    )
    await state.set_state(Registration.gender)

@router.message(Registration.gender)
async def process_gender(message: types.Message, state: FSMContext):
    """Обработка выбора пола"""
    gender_map = {
        "👨 Мужской": "male",
        "👩 Женский": "female",
        "⚪ Другое": "other"
    }
    
    if message.text not in gender_map:
        await message.answer("Пожалуйста, выберите пол из предложенных вариантов:")
        return
    
    await state.update_data(gender=gender_map[message.text])
    await message.answer(
        "Отправьте ваш номер телефона, нажав на кнопку ниже:",
        reply_markup=get_contact_keyboard()
    )
    await state.set_state(Registration.phone)

@router.message(Registration.phone)
async def process_phone(message: types.Message, state: FSMContext):
    """Обработка номера телефона"""
    if message.contact:
        phone = message.contact.phone_number
    else:
        # Если пользователь ввел номер вручную
        phone = message.text.strip()
        # Простая валидация номера (можно улучшить)
        if len(phone) < 10:
            await message.answer(
                "Пожалуйста, отправьте корректный номер телефона "
                "(используйте кнопку 'Отправить номер телефона'):"
            )
            return
    
    await state.update_data(phone=phone)
    await message.answer(
        "В каком городе ищем мероприятия?",
        reply_markup=get_city_keyboard()
    )
    await state.set_state(Registration.city)

@router.message(Registration.city)
async def process_city(message: types.Message, state: FSMContext):
    """Обработка выбора города"""
    city = message.text.strip()
    
    await state.update_data(city=city)
    
    # Сохраняем данные пользователя
    user_data = await state.get_data()
    user_id = message.from_user.id
    
    database.save_user(user_id, {
        'name': user_data['name'],
        'gender': user_data['gender'],
        'phone': user_data['phone'],
        'city': city
    })
    
    await message.answer(
        f"Отлично! Регистрация завершена ✅\n"
        f"Имя: {user_data['name']}\n"
        f"Город: {city}\n\n"
        "Теперь я могу помочь тебе найти интересные события!",
        reply_markup=get_main_menu()
    )
    
    await state.clear()