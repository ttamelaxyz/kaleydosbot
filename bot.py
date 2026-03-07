import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from states import Register, EventSearch
import keyboards as kb
import database as db

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):

    await message.answer(
        "Привет. Я бот, который поможет выбрать куда сходить.\n\n"
        "Давай зарегистрируемся.\nВведите ваше имя:"
    )

    await state.set_state(Register.name)


@dp.message(Register.name)
async def reg_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer("Введите ваш возраст:")
    await state.set_state(Register.age)


@dp.message(Register.age)
async def reg_age(message: Message, state: FSMContext):

    await state.update_data(age=message.text)

    await message.answer("Введите номер телефона:")
    await state.set_state(Register.phone)


@dp.message(Register.phone)
async def reg_phone(message: Message, state: FSMContext):

    data = await state.get_data()

    db.add_user(
        data["name"],
        data["age"],
        message.text
    )

    await message.answer(
        "Регистрация успешно завершена.",
        reply_markup=kb.main_menu
    )

    await state.clear()


# Подбор мероприятия

@dp.message(F.text == "Подобрать мероприятие")
async def choose_event(message: Message, state: FSMContext):

    await message.answer("Введите ваш бюджет:")
    await state.set_state(EventSearch.budget)


@dp.message(EventSearch.budget)
async def budget(message: Message, state: FSMContext):

    await state.update_data(budget=int(message.text))

    await message.answer(
        "Выберите тип мероприятия:",
        reply_markup=kb.places_keyboard
    )

    await state.set_state(EventSearch.place)


@dp.message(EventSearch.place)
async def place(message: Message, state: FSMContext):

    await state.update_data(place=message.text)

    await message.answer(
        "Какая атмосфера?",
        reply_markup=kb.atmosphere_keyboard
    )

    await state.set_state(EventSearch.atmosphere)


@dp.message(EventSearch.atmosphere)
async def atmosphere(message: Message, state: FSMContext):

    await state.update_data(atmosphere=message.text)

    await message.answer(
        "В какое время?",
        reply_markup=kb.time_keyboard
    )

    await state.set_state(EventSearch.time)


@dp.message(EventSearch.time)
async def time_choice(message: Message, state: FSMContext):

    data = await state.get_data()

    event = db.find_event(
        data["place"],
        data["atmosphere"],
        message.text,
        data["budget"]
    )

    if event:

        await message.answer(
            f"Предлагаю:\n\n{event[1]}",
            reply_markup=kb.event_actions
        )

        await state.update_data(link=event[6])

    else:

        await message.answer("Подходящих событий не найдено.")

    await state.clear()


@dp.message(F.text == "Ссылка на мероприятие")
async def event_link(message: Message, state: FSMContext):

    data = await state.get_data()

    await message.answer(data["link"])


# События города

@dp.message(F.text == "События в городе")
async def city_events(message: Message):

    events = db.city_events()

    text = "Главные события недели:\n\n"

    for e in events:
        text += f"{e[1]}\n{e[2]}\n\n"

    await message.answer(text)


# Случайное мероприятие

@dp.message(F.text == "Не хочу думать")
async def random_choice(message: Message):

    await message.answer_dice(emoji="🎲")
    await asyncio.sleep(4)

    event = db.random_event()

    await message.answer(
        f"Сегодня стоит сходить:\n\n{event[1]}"
    )


async def main():

    print("Бот запускается...")

    db.create_tables()

    print("Подключение к Telegram...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())