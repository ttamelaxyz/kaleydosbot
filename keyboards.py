from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Подобрать мероприятие")],
        [KeyboardButton(text="События в городе")],
        [KeyboardButton(text="Не хочу думать")]
    ],
    resize_keyboard=True
)

places_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кино")],
        [KeyboardButton(text="Театр")],
        [KeyboardButton(text="Выставка")],
        [KeyboardButton(text="Мастер-класс")],
        [KeyboardButton(text="Вечеринка")],
        [KeyboardButton(text="Концерт")]
    ],
    resize_keyboard=True
)

atmosphere_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Спокойная")],
        [KeyboardButton(text="Активная")]
    ],
    resize_keyboard=True
)

time_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="День")],
        [KeyboardButton(text="Вечер")]
    ],
    resize_keyboard=True
)

event_actions = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Другое мероприятие")],
        [KeyboardButton(text="Ссылка на мероприятие")],
        [KeyboardButton(text="Главное меню")]
    ],
    resize_keyboard=True
)