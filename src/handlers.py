from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram import types
from aiogram.utils.markdown import hbold

from parse import (
    get_become_a_resident,
    get_events,
    get_gov_services,
    get_technology_startup_accelerator,
    get_umnik,
    get_young_inventor_of_ugra
)
from keyboard import reply_keyboard, reply_contest_keyboard

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=reply_keyboard
    )


@router.message(F.text == "Помощь")
async def command_help_handler(message: types.Message) -> None:
    await message.answer("help", reply_markup=reply_keyboard)


@router.message(F.text == "Ближайшие мероприятия")
async def command_upcoming_events_handler(message: types.Message) -> None:
    await message.answer(await get_events(), reply_markup=reply_keyboard)


@router.message(F.text == "Государственные услуги")
async def command_gov_services_handler(message: types.Message) -> None:
    await message.answer(await get_gov_services(), reply_markup=reply_keyboard)


@router.message(F.text == "Как стать резидентом")
async def command_become_a_resident_handler(message: types.Message) -> None:
    await message.answer(await get_become_a_resident(), reply_markup=reply_keyboard)


@router.message(F.text == "Конкурсы")
async def command_contests_handler(message: types.Message) -> None:
    await message.answer("Выберите конкурс:", reply_markup=reply_contest_keyboard)


@router.message(F.text == "Конкурс «Акселератор технологических стартапов»")
async def command_technology_startup_accelerator_handler(message: types.Message) -> None:
    await message.answer(await get_technology_startup_accelerator(), reply_markup=reply_keyboard)


@router.message(F.text == "Конкурс «УМНИК»")
async def command_umnik_handler(message: types.Message) -> None:
    await message.answer(await get_umnik(), reply_markup=reply_keyboard)


@router.message(F.text == "Конкурс «Молодой изобретатель Югры»")
async def command_contests_handler(message: types.Message) -> None:
    await message.answer(await get_young_inventor_of_ugra(), reply_markup=reply_keyboard)
