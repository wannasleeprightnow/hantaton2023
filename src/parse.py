import aiohttp
import asyncio

from aiogram.utils.markdown import hbold
from bs4 import BeautifulSoup


async def get_events() -> str:
    response = ""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.tp86.ru/press-centr/events/") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            events = soup.find_all("a", {"class": "grid events__list_item"})
            for event in events:
                date = soup.find("p", {"class": "day text-color-black font-montserrat-weight-700 font-size-36"}).text.strip() + " "
                date += soup.find("p", {"class": "month"}).text.strip()
                title = soup.find("p", {"class": "prew-text text-color-black font-myriad-pro-weight-600 font-size-24 text-color-dark-purple events__list_item_prew-text"}).text.strip()
                link = "https://www.tp86.ru" + soup.find("a", {"class": "btn-2 adaptiveNameChange-js"})["href"]
                response += (f"""{hbold(title)}
Даты проведения: {date}
Подробная информация: {link}\n\n"""
                )
    return response


async def get_gov_services() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.tp86.ru/services/services/") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            gov_services = soup.find("div", {"class": "flex-list mt-40"}).find_all("p", {"class": "font-myriad-pro-weight-400 text-color-black font-size-17"})
    return '\n\n'.join([f"{number}. {service.text.strip()}." for number, service in enumerate(gov_services, start=1)])


async def get_become_a_resident() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.tp86.ru/residents/add/") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            criteria = []
            text = [soup.find("p", {"class": "font-size-22 mb-40 text-color-black font-myriad-pro-weight-400"}).text]
            criteria += soup.find_all("p", {"class": "two-column__item marker-gear font-size-22 text-color-black font-myriad-pro-weight-400 become-a-resident__marker-list__list-element"})
    return '\n\n'.join(text + [f"{number}. {criterion.text.strip()}" for number, criterion in enumerate(criteria, start=1)])


async def get_technology_startup_accelerator():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.tech-startups.ru/") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            fields = [
                "tn_text_1649505805859",  "tn_text_1649625899679", "tn_text_1680109165124",
                "tn_text_1680109165138", "tn_text_1680109165133", "tn_text_1680109165135",
                "tn_text_1680109165127", "tn_text_1680109165130", "tn_text_1649626787311",
                "tn_text_1649627009162", "tn_text_1649627084936", "tn_text_1649627103514",
                "tn_text_1649627110765", "tn_text_1649627110771", "tn_text_1680109490276",
                "tn_text_1680109490276", "tn_text_1649627889743","tn_text_1649628542930",
                "tn_text_1649628600528", "tn_text_1649628583857", "tn_text_1649628647594"
                ]
        info = [soup.find("div", {"class": "tn-atom", "field": field}).text.replace("\xa0", " ").capitalize() for field in fields]
        info[0] = hbold(info[0]) + ".\n"
        info[1] = hbold(info[1])
        info[7] += "\n"
        info[8] = hbold(info[8])
        info[15] += "\n"
        info[16] = hbold(info[16])
        info[2:8] = list(map(lambda x: " - " + x, info[2:8]))
        info[9:16] = list(map(lambda x: " - " + x, info[9:16]))
        info[17:23] = list(map(lambda x: " - " + x, info[17:23]))
        info.append(f"\n{hbold('Подробнее')}: https://www.tech-startups.ru/")
        return '\n'.join(info)


async def get_umnik():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://umnik.fasie.ru/") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            info = []
            info += soup.find("div", {"class": "b-pres_bl-1-1 b-pres_slide slide"}).find_all("p")
            info += soup.find("span", {"class": "b-pres_nav-item", "data-index": "2"})
            info += soup.find("ul", {"class": "slides", "id": "slides"}).find_all("p")
            info += soup.find("span", {"class": "b-pres_nav-item", "data-index": "3"})
            info += soup.find_all("li", {"class": "list-item"})
    info = list(filter(None, [i.text.replace("\xa0", " ").strip() for i in info if i.text]))
    info[0] = hbold(info[0])
    info[2] = hbold(info[2])
    info[17] = hbold(info[17])
    info[3] = " - " + info[3]
    info[5] = " - " + info[5]
    info[7] = " - " + info[7]
    info[9] = " - " + info[9]
    info[11] = " - " + info[11]
    info[13] = " - " + info[13]
    info[15] = " - " + info[15]
    info[18:24] = list(map(lambda x: " - " + x[:-1], info[18:24]))
    info.append(f"\n{hbold('Подробнее')}: https://umnik.fasie.ru/")
    return '\n\n'.join(info)


async def get_young_inventor_of_ugra():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://tp86.ru/molodoy-izobretatel-yugry/index.php") as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            info = []
            info += soup.find("h2", {"class": "raketa-info__info-title"})
            info += soup.find("h3", {"class": "deadlines__title"})
            info += soup.find_all("p", {"class": "deadlines__item-description"})
            info += soup.find("h4", {"class": "raketa-info__info-task-title"})
            info += soup.find("div", {"class": "raketa-info__info-task-container"}).find_all("p")
            info += soup.find("h3", {"class": "who-participant__title"})
            info += soup.find("div", {"class": "who-participant__container"}).find_all("p")
    info = [i.text.replace("\xa0", " ").replace("\n", "").replace("\t", "").strip() for i in info]
    info[0] = hbold(info[0])
    info[2] = " - " + info[2]
    info[3] = " - " + info[3]
    info[5] = " - " + info[5]
    info[6] = " - " + info[6]
    info[7] = " - " + info[7]
    info[9] = " - " + info[9]
    info[10] = " - " + info[10]
    info[11] = " - " + info[11]
    info[1] = hbold(info[1])
    info[4] = hbold(info[4])
    info[8] = hbold(info[8])
    info.append(f"\n{hbold('Подробнее')}: https://tp86.ru/molodoy-izobretatel-yugry/index.php")
    return "\n\n".join(info)
