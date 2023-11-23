import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import TOKEN
from handlers import router, send_news


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.get_event_loop().create_task(send_news(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
