# bot.py
# ============================================
# ОСНОВНОЙ ФАЙЛ БОТА
# ============================================

import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# Импортируем свои модули
from config import BOT_TOKEN, VIBE_MAP, TIME_MAP
from states import Registration, EventSelection
from keyboards import *
import database as db

# ====== ИНИЦИАЛИЗАЦИЯ ======
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ====== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======

async def show_event(event, chat_id, with_actions=True):
    """Показывает мероприятие пользователю"""
    message_text = f"🎉 <b>{event['title']}</b>\n\n"
    if 'date' in event:
        message_text += f"📅 {event['date']}\n"
    message_text += f"ℹ️ {event['description']}"
    
    if with_actions:
        await bot.send_message(
            chat_id, 
            message_text, 
            parse_mode="HTML",
            reply_markup=get_event_actions_keyboard(event['url'])
        )
    else:
        await bot.send_message(chat_id, message_text, parse_mode="HTML")

# ====== ОБРАБОТЧИКИ ======

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    """Приветствие и начало регистрации"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли пользователь в БД
    user = db.get_user(user_id)
    
    if user:
        db.update_user_activity(user_id)
        await message.answer(
            f"С возвращением, {user['name']}! 👋\n\n"
            "Куда отправимся сегодня?",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # Новая регистрация
    await message.answer(
        "👋 Привет! Я помогу тебе найти интересные события в городе.\n\n"
        "Давай сначала зарегистрируемся. Как тебя зовут?"
    )
    await state.set_state(Registration.name)

@dp.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    """Сохранение имени"""
    await state.update_data(name=message.text)
    await message.answer("Отлично! Сколько тебе лет?")
    await state.set_state(Registration.age)

@dp.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    """Сохранение возраста"""
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи возраст цифрами.")
        return
    
    await state.update_data(age=int(message.text))
    await message.answer(
        "Остался последний шаг — поделись номером телефона.",
        reply_markup=get_contact_keyboard()
    )
    await state.set_state(Registration.phone)

@dp.message(Registration.phone, F.contact)
async def process_phone(message: types.Message, state: FSMContext):
    """Завершение регистрации"""
    user_id = message.from_user.id
    contact = message.contact
    
    if contact.user_id != user_id:
        await message.answer("Пожалуйста, отправь свой номер телефона.")
        return
    
    data = await state.get_data()
    
    if db.add_user(user_id, data["name"], data["age"], contact.phone_number):
        db.log_action(user_id, "registration")
        await state.clear()
        
        await message.answer(
            f"✅ Регистрация успешно завершена, {data['name']}!\n\n"
            "Теперь ты можешь выбирать мероприятия:",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer(
            "😔 Ошибка при регистрации. Попробуй позже.",
            reply_markup=get_main_menu_keyboard()
        )

# ====== ГЛАВНОЕ МЕНЮ ======

@dp.message(F.text == "🎯 Подобрать мероприятие")
async def choose_event_start(message: types.Message, state: FSMContext):
    """Начало подбора мероприятия"""
    user_id = message.from_user.id
    db.update_user_activity(user_id)
    db.log_action(user_id, "start_selection")
    
    await message.answer(
        "Давай подберем мероприятие!\n"
        "Какой бюджет планируешь? (введи число в рублях)"
    )
    await state.set_state(EventSelection.budget)

@dp.message(EventSelection.budget)
async def process_budget(message: types.Message, state: FSMContext):
    """Обработка бюджета"""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer("Возвращаемся в меню.", reply_markup=get_main_menu_keyboard())
        return
    
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи число.")
        return
    
    await state.update_data(budget=int(message.text))
    await message.answer(
        "Какой тип мероприятия?",
        reply_markup=get_categories_keyboard()
    )
    await state.set_state(EventSelection.category)

@dp.message(EventSelection.category)
async def process_category(message: types.Message, state: FSMContext):
    """Обработка категории"""
    from config import CATEGORIES
    
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer("Возвращаемся в меню.", reply_markup=get_main_menu_keyboard())
        return
    
    if message.text not in CATEGORIES:
        await message.answer("Выбери из списка.", reply_markup=get_categories_keyboard())
        return
    
    await state.update_data(category=message.text)
    await message.answer(
        "Какая атмосфера?",
        reply_markup=get_vibe_keyboard()
    )
    await state.set_state(EventSelection.vibe)

@dp.message(EventSelection.vibe)
async def process_vibe(message: types.Message, state: FSMContext):
    """Обработка атмосферы"""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer("Возвращаемся в меню.", reply_markup=get_main_menu_keyboard())
        return
    
    if message.text not in VIBE_MAP:
        await message.answer("Выбери из списка.", reply_markup=get_vibe_keyboard())
        return
    
    await state.update_data(vibe=VIBE_MAP[message.text])
    await message.answer(
        "В какое время?",
        reply_markup=get_time_keyboard()
    )
    await state.set_state(EventSelection.time)

@dp.message(EventSelection.time)
async def process_time(message: types.Message, state: FSMContext):
    """Завершение подбора и показ мероприятия"""
    if message.text == "🏠 Главное меню":
        await state.clear()
        await message.answer("Возвращаемся в меню.", reply_markup=get_main_menu_keyboard())
        return
    
    if message.text not in TIME_MAP:
        await message.answer("Выбери из списка.", reply_markup=get_time_keyboard())
        return
    
    data = await state.get_data()
    time = TIME_MAP[message.text]
    
    # Ищем событие в БД
    event = db.get_random_filtered_event(
        data['budget'],
        data['category'],
        data['vibe'],
        time
    )
    
    if event:
        db.log_action(message.from_user.id, "event_found", event['id'])
        await show_event(event, message.chat.id, with_actions=True)
        await state.update_data(search_params={
            "budget": data['budget'],
            "category": data['category'],
            "vibe": data['vibe'],
            "time": time
        })
    else:
        await message.answer(
            "😔 Ничего не найдено. Попробуй другие параметры.",
            reply_markup=get_back_to_menu_keyboard()
        )

@dp.message(F.text == "📅 События в городе")
async def weekly_events(message: types.Message):
    """Показывает событие из еженедельной подборки"""
    user_id = message.from_user.id
    db.update_user_activity(user_id)
    db.log_action(user_id, "weekly_events")
    
    event = db.get_random_weekly_event()
    if event:
        await show_event(event, message.chat.id, with_actions=True)
    else:
        await message.answer(
            "😔 На этой неделе пока нет событий.",
            reply_markup=get_back_to_menu_keyboard()
        )

@dp.message(F.text == "🎲 Не хочу думать")
async def random_event(message: types.Message):
    """Случайное мероприятие с кубиком"""
    user_id = message.from_user.id
    db.update_user_activity(user_id)
    db.log_action(user_id, "random_event")
    
    msg = await message.answer_dice(emoji="🎲")
    await asyncio.sleep(2)
    
    event = db.get_random_event()
    if event:
        await show_event(event, message.chat.id, with_actions=True)
    else:
        await message.answer(
            "😔 В базе пока нет событий.",
            reply_markup=get_back_to_menu_keyboard()
        )

@dp.message(F.text == "🏠 Главное меню")
async def go_to_main_menu(message: types.Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    user = db.get_user(message.from_user.id)
    
    if user:
        await message.answer(
            f"Главное меню, {user['name']}:",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

# ====== ОБРАБОТЧИКИ ИНЛАЙН КНОПОК ======

@dp.callback_query(F.data == "another_event")
async def another_event(callback: types.CallbackQuery, state: FSMContext):
    """Показать другое мероприятие"""
    await callback.answer()
    
    data = await state.get_data()
    search_params = data.get('search_params')
    
    if search_params:
        event = db.get_random_filtered_event(
            search_params['budget'],
            search_params['category'],
            search_params['vibe'],
            search_params['time']
        )
        if event:
            await show_event(event, callback.message.chat.id, with_actions=True)
        else:
            await callback.message.answer(
                "😔 Больше нет мероприятий.",
                reply_markup=get_back_to_menu_keyboard()
            )
    else:
        await callback.message.answer(
            "Начни поиск заново.",
            reply_markup=get_main_menu_keyboard()
        )

@dp.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await callback.answer()
    await state.clear()
    
    user = db.get_user(callback.from_user.id)
    if user:
        await callback.message.answer(
            f"Главное меню, {user['name']}:",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

# ====== ЗАПУСК ======

async def main():
    print("🚀 Бот запущен...")
    print("📊 База данных: database/bot_database.db")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())