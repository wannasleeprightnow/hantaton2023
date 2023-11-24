import datetime
from typing import Iterable

from aiogram.utils.markdown import bold

from parse import Parser

parser = Parser()


class Service:

    def __init__(self):
        self._formated_events: str = ""
        self._formated_important_news: list = []
        self._formated_gov_services: str = ""
        self._formated_become_a_resident: str = ""
        self._formated_technology_startup_accelerator: str = ""
        self._formated_umnik: str = ""
        self._formated_young_inventor_of_ugra: str = ""
        self._last_formating_time: float = 0
        self._last_news_time: float = 0

    async def _check_last_formating_time(self):
        delta = datetime.datetime.now().timestamp() - self._last_formating_time
        if delta > 3600 or delta < 1:
            await self._format_all()
            self._last_formating_time = datetime.datetime.now().timestamp()

    async def _check_last_news_time(self) -> None | bool:
        delta = datetime.datetime.now().timestamp() - self._last_news_time
        last_news = await self._format_important_news()
        if 1000000 > delta > 43200 and not (
                    last_news in self._formated_important_news):
            self._formated_important_news.extend(last_news)
            self._last_news_time = datetime.datetime.now().timestamp()
            return True

    async def _format_all(self):
        try:
            # raise Exception
            await self._format_events()
            await self._format_gov_services()
            await self._format_become_a_resident()
            await self._format_technology_startup_accelerator()
            await self._format_umnik()
            await self._format_young_inventor_of_ugra()
        except Exception:
            ...

    async def _numerate(self, indixes: Iterable[int], sequence: list) -> list:
        for number, i in enumerate(indixes, start=1):
            sequence[i] = f"{number}. {sequence[i]}"
        return sequence

    async def _bold(self, indixes: Iterable[int], sequence: list) -> list:
        for i in indixes:
            sequence[i] = bold(sequence[i])
        return sequence

    async def _add_empty_line(self, indixes: Iterable[int], sequence: list
                              ) -> list:
        for i in indixes:
            sequence[i] += "\n"
        return sequence

    async def events(self):
        await self._check_last_formating_time()
        return self._formated_events

    async def important_news(self):
        if await self._check_last_news_time():
            return self._formated_important_news.pop(0)

    async def gov_services(self):
        await self._check_last_formating_time()
        return self._formated_gov_services

    async def become_a_resident(self):
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
Подробнее: {event.link}\n\n"""
                                )
        self._formated_events = formated_events

    async def _format_important_news(self) -> list:
        important_news = await parser.get_important_news()
        formated_important_news = []
        for one_news in important_news:
            formated_important_news.append(f"""{one_news.date}\n
{one_news.title}\n
Подробнее: {one_news.link}""")
        return formated_important_news

    async def _format_gov_services(self) -> None:
        gov_services = await parser.get_gov_services()
        gov_services = [
            f"{number}. {service}."
            for number, service in enumerate(gov_services, start=1)
            ]
        self._formated_gov_services = "\n\n".join(gov_services)

    async def _format_become_a_resident(self) -> None:
        criteria = await parser.get_become_a_resident()
        criteria = [
            f"{number}. {criterion.strip()}."
            for number, criterion in enumerate(criteria, start=1)
        ]
        self._formated_become_a_resident = "\n\n".join(criteria)

    async def _format_technology_startup_accelerator(self) -> None:
        contest_info = await parser.get_technology_startup_accelerator()
        contest_info = await self._bold((0, 1, 8, 16), contest_info)
        contest_info = await self._numerate(list(range(2, 8)), contest_info)
        contest_info = await self._numerate(list(range(9, 16)), contest_info)
        contest_info = await self._numerate(list(range(17, 21)), contest_info)
        contest_info = await self._add_empty_line((0, 7, 15), contest_info)
        self._formated_technology_startup_accelerator = "\n".join(contest_info)

    async def _format_umnik(self) -> None:
        contest_info = await parser.get_umnik()
        contest_info = await self._bold((0, 2, 17), contest_info)
        contest_info = await self._numerate(
            (3, 5, 7, 9, 11, 13, 15), contest_info)
        contest_info = await self._numerate(list(range(18, 24)), contest_info)
        contest_info = await self._add_empty_line((1, 9, 16, 23), contest_info)
        self._formated_umnik = "\n".join(contest_info)

    async def _format_young_inventor_of_ugra(self) -> None:
        contest_info = await parser.get_young_inventor_of_ugra()
        contest_info = await self._bold((0, 1, 4, 8), contest_info)
        contest_info = await self._numerate((2, 3), contest_info)
        contest_info = await self._numerate((5, 6, 7), contest_info)
        contest_info = await self._numerate((9, 10, 11), contest_info)
        contest_info = await self._add_empty_line((0, 3, 7, 11), contest_info)
        self._formated_young_inventor_of_ugra = "\n".join(contest_info)
