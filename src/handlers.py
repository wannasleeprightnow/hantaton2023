from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart
from aiogram.utils.markdown import bold
from asyncio import sleep

from keyboard import reply_keyboard, reply_contest_keyboard
from db.database import execute, fetch_all
from db.sql import ADD_USER, GET_USERS
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
    await message.answer("help", reply_markup=reply_keyboard)


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
async def command_technology_startup_accelerator_handler(message: types.Message) -> None:
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


async def send_news(bot: Bot):
    while True:
        if news := await service.important_news():
            if users := await fetch_all(GET_USERS):
                for user_id in users:
                    await bot.send_message(chat_id=str(user_id[0]), text=news)
        await sleep(120)
