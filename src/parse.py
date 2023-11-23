import aiohttp

from bs4 import BeautifulSoup

from schemas import Event, News


class Parser:

    async def _get_html_page(self, url) -> BeautifulSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                soup = BeautifulSoup(await resp.text(), "html.parser")
                return soup

    async def _to_text(self, info: list) -> list[str]:
        return list(filter(None, [i.text.replace("\xa0", " ")
                .replace("\n", "").replace("\t", "").strip() for i in info]))

    async def get_events(self) -> list[Event]:
        events_info = []
        soup = await self._get_html_page(
            "https://www.tp86.ru/press-centr/events/"
            )

        all_events = soup.find_all("a", {"class": "grid events__list_item"})
        for _ in range(len(all_events)):

            date = soup.find(
                "p",
                {"class": "day text-color-black font-montserrat-weight-700 font-size-36"}).text.strip() + " "
            date += soup.find("p", {"class": "month"}).text.strip()
            title = soup.find(
                "p",
                {"class": "prew-text text-color-black font-myriad-pro-weight-600 font-size-24 text-color-dark-purple events__list_item_prew-text"}).text.strip()
            link = "https://www.tp86.ru" + soup.find(
                "a", {"class": "btn-2 adaptiveNameChange-js"})["href"]

            events_info.append(Event(date=date, title=title, link=link))
        return events_info

    async def get_gov_services(self) -> list[str]:
        soup = await self._get_html_page(
            "https://www.tp86.ru/services/services/")

        gov_services = soup.find(
            "div",
            {"class": "flex-list mt-40"}).find_all("p", {"class":
                "font-myriad-pro-weight-400 text-color-black font-size-17"})
        return await self._to_text(gov_services)

    async def get_become_a_resident(self) -> list[str]:
        soup = await self._get_html_page("https://www.tp86.ru/residents/add/")

        header = [soup.find("p",
                            {"class": "font-size-22 mb-40 text-color-black font-myriad-pro-weight-400"}).text.strip()]
        criteria = soup.find_all(
            "p",
            {"class": "two-column__item marker-gear font-size-22 text-color-black font-myriad-pro-weight-400 become-a-resident__marker-list__list-element"})
        return header + await self._to_text(criteria)

    async def get_technology_startup_accelerator(self) -> list[str]:
        soup = await self._get_html_page("https://www.tech-startups.ru/")
        contest_info = []
        fields = [
                "tn_text_1649505805859",  "tn_text_1649625899679",
                "tn_text_1680109165124", "tn_text_1680109165138",
                "tn_text_1680109165133", "tn_text_1680109165135",
                "tn_text_1680109165127", "tn_text_1680109165130",
                "tn_text_1649626787311", "tn_text_1649627009162",
                "tn_text_1649627084936", "tn_text_1649627103514",
                "tn_text_1649627110765", "tn_text_1649627110771",
                "tn_text_1680109490276", "tn_text_1680109490276",
                "tn_text_1649627889743", "tn_text_1649628542930",
                "tn_text_1649628600528", "tn_text_1649628583857",
                "tn_text_1649628647594"
                ]

        contest_info = await self._to_text(
            [soup.find("div", {"class": "tn-atom",
                               "field": field}) for field in fields])

        contest_info.append("Подробнее: https://www.tech-startups.ru/")
        return contest_info

    async def get_umnik(self) -> list[str]:
        soup = await self._get_html_page("https://umnik.fasie.ru/")
        contest_info = []

        contest_info += soup.find("div", {
            "class": "b-pres_bl-1-1 b-pres_slide slide"}).find_all("p")
        contest_info += soup.find("span", {
            "class": "b-pres_nav-item", "data-index": "2"})
        contest_info += soup.find("ul", {
            "class": "slides", "id": "slides"}).find_all("p")
        contest_info += soup.find("span", {
            "class": "b-pres_nav-item", "data-index": "3"})
        contest_info += soup.find_all("li", {
            "class": "list-item"})

        contest_info = await self._to_text(contest_info)
        contest_info.append("Подробнее: https://umnik.fasie.ru/")
        return contest_info

    async def get_young_inventor_of_ugra(self) -> list[str]:
        soup = await self._get_html_page(
            "https://tp86.ru/molodoy-izobretatel-yugry/index.php")
        contest_info = []

        contest_info += soup.find("h2", {"class": "raketa-info__info-title"})
        contest_info += soup.find("h3", {"class": "deadlines__title"})
        contest_info += soup.find_all("p", {"class":
            "deadlines__item-description"})
        contest_info += soup.find("h4", {"class":
            "raketa-info__info-task-title"})
        contest_info += soup.find("div", {"class":
            "raketa-info__info-task-container"}).find_all("p")
        contest_info += soup.find("h3", {"class":
            "who-participant__title"})
        contest_info += soup.find("div", {"class":
            "who-participant__container"}).find_all("p")

        contest_info = await self._to_text(contest_info)

        contest_info.append(
            "Подробнее: https://tp86.ru/molodoy-izobretatel-yugry/index.php")
        return contest_info

    async def get_important_news(self) -> list[News]:
        soup = await self._get_html_page(
            "https://www.tp86.ru/press-centr/news/")
        news_info = []

        with open("words.txt") as file:
            file = [i.strip().lower() for i in file.readlines()]

        news = soup.find_all("a", {"class": "news-element news__list_item"})

        for one_news in news:
            news_title = one_news.find("p", {"class": "news-element_text-prew font-myriad-pro-weight-400 font-size-22 text-color-black mb-20"}).text.strip()
            news_date = one_news.find("p", {"class": "news-element_date-day font-myriad-pro-weight-700 text-color-purple mt-40 font-size-36"}).text.strip() + " "
            news_date += one_news.find("p", {"class": "news-element_date-month font-montserrat-weight-400 font-size-16 mb-15"}).text.strip()
            news_link = "https://www.tp86.ru/press-centr/news" + one_news["href"]

            if set(file) & set(news_title.lower().split(" ")):
                news_info.append(News(news_title, news_date, news_link))

        return news_info
