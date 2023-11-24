from aiogram import Bot, F, Router, types
from aiogram.filters import Command,  CommandStart
from aiogram.utils.markdown import bold
from asyncio import sleep

from keyboard import (
    admin_reply_keyboard,
    reply_keyboard,
    reply_contest_keyboard
)
from db.database import execute, fetch_all
from db.sql import ADD_USER, ADD_ADMIN, GET_ADMINS, GET_USERS
from service import Service

router = Router()
service = Service()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Hello, {bold(message.from_user.full_name)}!",
        reply_markup=reply_keyboard
    )
    await execute(ADD_USER, (message.from_user.id,))


@router.message(F.text == "Помощь")
async def command_help_handler(message: types.Message) -> None:
    await message.answer(
        "Привет, я бот Технопарка Югры! \
Все команды доступны в reply-клавиатуре.",
        reply_markup=reply_keyboard
        )


@router.message(F.text == "Ближайшие мероприятия")
async def command_upcoming_events_handler(message: types.Message) -> None:
    await message.answer(await service.events(), reply_markup=reply_keyboard)


@router.message(F.text == "Государственные услуги")
async def command_gov_services_handler(message: types.Message) -> None:
    await message.answer(
        await service.gov_services(), reply_markup=reply_keyboard
        )


@router.message(F.text == "Как стать резидентом")
async def command_become_a_resident_handler(message: types.Message) -> None:
    await message.answer(
        await service.become_a_resident(), reply_markup=reply_keyboard
        )


@router.message(F.text == "Конкурсы")
async def command_contests_handler(message: types.Message) -> None:
    await message.answer(
        "Выберите конкурс:", reply_markup=reply_contest_keyboard
        )


@router.message(F.text == "Конкурс «Акселератор технологических стартапов»")
async def command_technology_startup_accelerator_handler(
    message: types.Message) -> None:
    await message.answer(
        await service.technology_startup_accelerator(),
        reply_markup=reply_keyboard
        )


@router.message(F.text == "Конкурс «УМНИК»")
async def command_umnik_handler(message: types.Message) -> None:
    await message.answer(await service.umnik(), reply_markup=reply_keyboard)


@router.message(F.text == "Конкурс «Молодой изобретатель Югры»")
async def command_young_inventor_of_ugra_handler(message: types.Message
                                                 ) -> None:
    await message.answer(
        await service.young_inventor_of_ugra(), reply_markup=reply_keyboard)


@router.message(F.text == "Назад")
async def command_back_handler(message: types.Message) -> None:
    await message.answer("Назад!", reply_markup=reply_keyboard)


@router.message(Command("admin"))
async def command_admin_handler(message: types.Message) -> None:
    if await is_admin(message.from_user.id):
        await message.answer(
            "Вы перешли в режим админа!", reply_markup=admin_reply_keyboard)


@router.message(F.text == "Помощь для администратора")
async def command_help_for_admin_handler(message: types.Message) -> None:
    if await is_admin(message.from_user.id):
        await message.answer(f"""{bold('Вот команды, которые доступны для администратора:')}

- Добавить администратора /ид пользователя/ . Чтобы это сработало, пользователь должен прописать /start в этом боте.

Дальнейшие команды нужны для ручной настройки бота. Именно в таком виде пользователям будут приходить сообщения

- Изменить ближайшие мероприятия
/список мероприятий/

- Изменить важные новости
/новость/

- Изменить государственные услуги
/список государственных услуг/

- Изменить как стать резидентом
/как стать резидентом/

- Изменить конкурс «Акселератор технологических стартапов»
/новая информация о конкурсе/

- Изменить конкурс «УМНИК»
/новая информация о конкурсе/

- Изменить конкурс «Молодой изобретатель Югры»
/новая информация о конкурсе/
""", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith("Добавить администратора"))
async def command_add_admin_handler(message: types.Message) -> None:
    user_id = int(message.text.split()[-1])
    try:
        await execute(ADD_ADMIN, (user_id, ))
        await message.answer("Пользователь добавлен в список администраторов!")
    except Exception:
        await message.answer("Что-то пошло не так!")


@router.message(F.text.startswith("Изменить ближайшие мероприятия"))
async def command_set_events_handler(message: types.Message) -> None:
    service._formated_events = await set_new_data(message)
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith("Изменить важные новости"))
async def command_set_important_news_handler(message: types.Message) -> None:
    service._formated_important_news.append(await set_new_data(message))
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith("Изменить государственные услуги"))
async def command_set_gov_services_handler(message: types.Message) -> None:
    service._formated_gov_services = await set_new_data(message)
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith("Изменить как стать резидентом"))
async def command_set_become_a_resident_handler(
            message: types.Message) -> None:
    service._formated_become_a_resident = await set_new_data(message)
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith("Изменить конкурс «Акселератор\
    технологических стартапов»"))
async def command_set_technology_startup_accelerator_handler(
            message: types.Message) -> None:
    service._formated_technology_startup_accelerator = await set_new_data(
                                                                    message)
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith("Изменить конкурс «УМНИК»"))
async def command_set_umnik_handler(message: types.Message) -> None:
    service._formated_umnik = await set_new_data(message)
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


@router.message(F.text.startswith(
    "Изменить конкурс «Молодой изобретатель Югры»"))
async def command_set_young_inventor_of_ugra_handler(
    message: types.Message) -> None:
    service._formated_young_inventor_of_ugra = await set_new_data(message)
    await message.answer("Успешно!", reply_markup=admin_reply_keyboard)


async def set_new_data(message):
    if await is_admin(message.from_user.id):
        return '\n'.join(message.text.split("\n")[1:])


async def is_admin(user_id):
    all_admins_ids = [admin_id[0] for admin_id in await fetch_all(GET_ADMINS)]
    if user_id in all_admins_ids:
        return True
    return False


async def send_news(bot: Bot):
    while True:
        if news := await service.important_news():
            if users := await fetch_all(GET_USERS):
                for user_id in users:
                    await bot.send_message(chat_id=str(user_id[0]), text=news)
        await sleep(120)
