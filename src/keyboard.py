from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Ближайшие мероприятия")],
        [KeyboardButton(text="Государственные услуги")],
        [KeyboardButton(text="Как стать резидентом")],
        [KeyboardButton(text="Конкурсы")],
    ],
    resize_keyboard=True,
)

reply_contest_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text="Конкурс «Акселератор технологических стартапов»")],
        [KeyboardButton(text="Конкурс «УМНИК»")],
        [KeyboardButton(text="Конкурс «Молодой изобретатель Югры»")]
    ],
    resize_keyboard=True,
)
