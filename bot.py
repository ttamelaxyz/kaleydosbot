import asyncio
import random
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import database as db
import keyboards as kb

from states import Register, Search, AddEvent
from config import TOKEN, ADMIN_ID


bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

user_events = {}


# ---------------- START ----------------

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):

    user = db.user_exists(message.from_user.id)

    if user:

        name = user[2]

        await message.answer(
            f"С возвращением, {name} 👋",
            f"Подберем лучшее событие для тебя?",
            reply_markup=kb.main_menu()
        )

    else:

        await message.answer(
            "Добро пожаловать в kaleydosbot\n"
            "Я помогу тебе выбраться из дома, найти классные события и собрать маршрут по городу.\n\n"
            "Давайте коротко заполним профиль, чтобы я мог лучше подобрать идеи?"
        )

        await state.set_state(Register.name)


# ---------------- REGISTRATION ----------------

@dp.message(Register.name)
async def reg_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Укажи свой пол:",
        reply_markup=keyboard
    )

    await state.set_state(Register.gender)


@dp.message(Register.gender)
async def reg_gender(message: Message, state: FSMContext):

    await state.update_data(gender=message.text)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер", request_contact=True)]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Нажми кнопку, чтобы отправить номер телефона:",
        reply_markup=keyboard
    )

    await state.set_state(Register.phone)


@dp.message(Register.phone, F.contact)
async def reg_phone(message: Message, state: FSMContext):

    data = await state.get_data()

    phone = message.contact.phone_number

    db.add_user(
        message.from_user.id,
        data["name"],
        data["gender"],
        phone
    )

    await message.answer(
        "Регистрация завершена ✅",
        reply_markup=kb.main_menu()
    )

    await state.clear()


# ---------------- SEARCH ----------------

@dp.message(F.text == "🎯 Подобрать мероприятие")
async def search(message: Message, state: FSMContext):

    await message.answer("Мне нужно немного информации, чтобы подобрать идеи. Ответьте на несколько вопросов\n\nВведите бюджет на одного человека:")

    await state.set_state(Search.budget)


@dp.message(Search.budget)
async def budget(message: Message, state: FSMContext):

    if not message.text.isdigit():
        return

    budget = int(message.text)

    await state.update_data(budget=budget)

    await message.answer(
        "Выберите тип мероприятия:",
        reply_markup=kb.places()
    )

    await state.set_state(Search.place)


@dp.message(Search.place, F.text.in_([
    "Кино", "Концерт", "Выставка",
    "Мастер-класс", "Вечеринка",
    "Театры и стендапы"
]))
async def place(message: Message, state: FSMContext):

    await state.update_data(place=message.text)

    await message.answer(
        "Какая атмосфера важнее?",
        reply_markup=kb.atmosphere()
    )
    await state.set_state(Search.atmosphere)


@dp.message(Search.atmosphere, F.text.in_(["Спокойная", "Активная"]))
async def atmosphere(message: Message, state: FSMContext):

    await state.update_data(atmosphere=message.text)

    await message.answer(
        "Когда планируете пойти?",
        reply_markup=kb.time()
    )
    await state.set_state(Search.time)


@dp.message(Search.time, F.text.in_(["День", "Вечер"]))
async def time(message: Message, state: FSMContext):

    data = await state.get_data()

    events = db.find_events(
        data["place"],
        data["atmosphere"],
        message.text,
        data["budget"]
    )

    if not events:

        await message.answer("Подходящих мероприятий не найдено.")
        await message.answer(
            "Главное меню",
            reply_markup=kb.main_menu()
        )
        return

    user_events[message.from_user.id] = events

    event = random.choice(events)

    await send_event(message.chat.id, event)

    await state.update_data(current=event)
    await state.clear()


# ---------------- EVENT ----------------

async def send_event(chat_id, event):

    image = event[8]

    text = (
        f"🎫 {event[1]}\n\n"
        f"{event[2]}\n\n"
        f"💰 Бюджет: до {event[6]}"
    )

    if event[7]:
        text += f"\n\n🔗 {event[7]}"

    photo = FSInputFile(image)

    await bot.send_photo(
        chat_id,
        photo,
        caption=text,
        reply_markup=kb.event_buttons()
    )


# ---------------- NEXT EVENT ----------------

@dp.message(F.text == "🔁 Другое мероприятие")
async def next_event(message: Message):

    events = user_events.get(message.from_user.id)

    if not events:
        return

    event = random.choice(events)

    await send_event(message.chat.id, event)


# ---------------- CITY EVENTS ----------------

import os
from aiogram.types import InputMediaPhoto


@dp.message(F.text == "🏙 События недели")
async def city_events(message: Message):

    folder = "images/week_events"

    images = os.listdir(folder)

    if not images:
        await message.answer("Пока нет событий недели.")
        return

    media = []

    description = (
        "А вот и подборка мероприятий на неделю💞\n\n"
        "В программе концерт легендарной группы, захватывающий вечер в космической обсерватории"
        "и даже стендап с сюрпризом🎶\n\n"
        "Выбирай формат под настроение или для компании 😉 "
    )

    for i, img in enumerate(images):

        path = f"{folder}/{img}"

        photo = FSInputFile(path)

        if i == 0:
            media.append(
                InputMediaPhoto(
                    media=photo,
                    caption=description
                )
            )
        else:
            media.append(
                InputMediaPhoto(media=photo)
            )

    await bot.send_media_group(
        message.chat.id,
        media
    )


# ---------------- RANDOM ----------------

@dp.message(F.text == "🎲 Случайное событие")
async def random_event(message: Message):

    await bot.send_dice(message.chat.id, emoji="🎲")

    await asyncio.sleep(3)

    event = db.random_event()

    if not event:

        await message.answer("Событий пока нет.")
        return

    await send_event(message.chat.id, event)


# ---------------- MENU ----------------

@dp.message(F.text == "🏠 Главное меню")
async def menu(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Главное меню",
        reply_markup=kb.main_menu()
    )


# ---------------- ADMIN PANEL ----------------

@dp.message(Command("addevent"))
async def add_event(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("Название события")

    await state.set_state(AddEvent.name)


@dp.message(AddEvent.name)
async def admin_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer("Описание")

    await state.set_state(AddEvent.description)


@dp.message(AddEvent.description)
async def admin_description(message: Message, state: FSMContext):

    await state.update_data(description=message.text)

    await message.answer("Тип мероприятия")

    await state.set_state(AddEvent.place)


@dp.message(AddEvent.place)
async def admin_place(message: Message, state: FSMContext):

    await state.update_data(place=message.text)

    await message.answer("Атмосфера")

    await state.set_state(AddEvent.atmosphere)


@dp.message(AddEvent.atmosphere)
async def admin_atm(message: Message, state: FSMContext):

    await state.update_data(atmosphere=message.text)

    await message.answer("Время")

    await state.set_state(AddEvent.time)


@dp.message(AddEvent.time)
async def admin_time(message: Message, state: FSMContext):

    await state.update_data(time=message.text)

    await message.answer("Бюджет")

    await state.set_state(AddEvent.budget)


@dp.message(AddEvent.budget)
async def admin_budget(message: Message, state: FSMContext):

    await state.update_data(budget=int(message.text))

    await message.answer("Ссылка (если нет — напиши 'нет')")

    await state.set_state(AddEvent.link)


@dp.message(AddEvent.link)
async def admin_link(message: Message, state: FSMContext):

    link = message.text

    if link.lower() in ["нет", "-", "no"]:
        link = None

    await state.update_data(link=link)

    await message.answer("Отправь изображение")

    await state.set_state(AddEvent.image)


@dp.message(AddEvent.image)
async def admin_image(message: Message, state: FSMContext):

    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    path = f"images/{photo.file_id}.jpg"

    await bot.download_file(file.file_path, path)

    data = await state.get_data()

    db.add_event(
        data["name"],
        data["description"],
        data["place"],
        data["atmosphere"],
        data["time"],
        data["budget"],
        data["link"],
        path
    )

    await message.answer("Событие добавлено ✅")

    await state.clear()


# ---------------- START BOT ----------------

async def main():

    db.create_tables()

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())