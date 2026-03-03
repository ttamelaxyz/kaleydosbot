from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_main_menu, get_city_keyboard
from utils.states import Registration
import database

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    # Проверяем, зарегистрирован ли пользователь
    user = database.get_user(user_id)
    
    if user:
        # Если пользователь уже есть, показываем главное меню
        await message.answer(
            f"С возвращением, {user['name']}! 👋\n"
            "Я помогу тебе найти интересные события в твоем городе.",
            reply_markup=get_main_menu()
        )
    else:
        # Начинаем регистрацию
        await message.answer(
            "Привет! 👋\n"
            "Я бот-помощник для поиска мероприятий в твоем городе.\n"
            "Давай познакомимся! Как тебя зовут?"
        )
        await state.set_state(Registration.name)