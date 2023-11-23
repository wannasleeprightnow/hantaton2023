import asyncio
import datetime

from aiogram.utils.markdown import bold

from parse import Parser

parser = Parser()


class View:

    def __init__(self):
        self._formated_events: str = ""
        self._formated_gov_services: str = ""
        self._formated_become_a_resident: str = ""
        self._formated_technology_startup_accelerator: str = ""
        self._formated_umnik: str = ""
        self._formated_young_inventor_of_ugra: str = ""
        self._last_formating_time: float = 0

    async def _check_last_formating_time(self):
        delta = datetime.datetime.now().timestamp() - self._last_formating_time
        if not (3 > delta > 3600):
            await self._format_all()
            self._last_formating_time = datetime.datetime.now().timestamp()

    async def _format_all(self):
        try:
            await self._format_events()
            await self._format_gov_services()
            await self._format_become_a_residen()
            await self._format_technology_startup_accelerator()
            await self._format_umnik()
            await self._format_young_inventor_of_ugra()
            self._last_formating_time = datetime.datetime.now().timestamp()

        except Exception:
            ...

    async def events(self):
        await self._check_last_formating_time()
        return self._formated_events

    async def gov_services(self):
        await self._check_last_formating_time()
        return self._formated_gov_services

    async def become_a_residen(self):
        await self._check_last_formating_time()
        return self._formated_become_a_resident

    async def technology_startup_accelerator(self):
        await self._check_last_formating_time()
        return self._formated_technology_startup_accelerator

    async def umnik(self):
        await self._check_last_formating_time()
        return self._formated_umnik

    async def young_inventor_of_ugra(self):
        await self._check_last_formating_time()
        return self._formated_young_inventor_of_ugra

    async def _format_events(self) -> None:
        events = await parser.get_events()
        formated_events = ""
        for event in events:
            formated_events += (f"""{bold(event.title)}
Даты проведения: {event.date}
Подробная информация: {event.link}\n\n"""
                                )
        self._formated_events = formated_events

    async def _format_gov_services(self) -> None:
        gov_services = await parser.get_gov_services()
        gov_services = [
            f"{number}. {service}."
            for number, service in enumerate(gov_services, start=1)
            ]
        self._formated_gov_services = "\n\n".join(gov_services)

    async def _format_become_a_residen(self) -> None:
        criteria = await parser.get_become_a_resident()
        criteria = [
            f"{number}. {criterion.strip()}."
            for number, criterion in enumerate(criteria, start=1)
        ]
        self._formated_become_a_resident = "\n\n".join(criteria)

    async def _format_technology_startup_accelerator(self) -> None:
        contest_info = await parser.get_technology_startup_accelerator()
        for i in (0, 1, 8, 16):
            contest_info[i] = bold(contest_info[i])
        contest_info[2:8] = [
            f"{number}. {info}."
            for number, info in enumerate(contest_info[2:8], start=1)
            ]
        contest_info[9:16] = [
            f"{number}. {info}."
            for number, info in enumerate(contest_info[9:16], start=1)
            ]
        contest_info[17:21] = [
            f"{number}. {info}."
            for number, info in enumerate(contest_info[17:21], start=1)
            ]
        for i in (0, 7, 15, 2):
            contest_info[i] += "\n"
        self._formated_technology_startup_accelerator = "\n".join(contest_info)

    async def _format_umnik(self) -> None:
        contest_info = await parser.get_umnik()
        for i in (0, 2, 17):
            contest_info[i] = bold(contest_info[i])
        for number, i in enumerate((3, 5, 7, 9, 11, 13, 15), start=1):
            contest_info[i] = f"{number}. {contest_info[i]}"
        contest_info[18:24] = [
            f"{number}. {info[:-1]}."
            for number, info in enumerate(contest_info[18:24], start=1)
            ]
        self._formated_umnik = "\n\n".join(contest_info)

    async def _format_young_inventor_of_ugra(self) -> None:
        contest_info = await parser.get_young_inventor_of_ugra()
        for i in (0, 1, 4, 8):
            contest_info[i] = bold(contest_info[i])
        for number, i in enumerate((2, 3), start=1):
            contest_info[i] = f"{number}. {contest_info[i]}"
        for number, i in enumerate((5, 6, 7), start=1):
            contest_info[i] = f"{number}. {contest_info[i]}"
        for number, i in enumerate((9, 10, 11), start=1):
            contest_info[i] = f"{number}. {contest_info[i]}"
        self._formated_young_inventor_of_ugra = "\n\n".join(contest_info)
