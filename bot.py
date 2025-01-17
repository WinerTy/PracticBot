from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from routers import get_router
from logger import logger


# Функция для запуска бота
async def main() -> None:
    bot = Bot(token=config.bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(await get_router())

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(e)
    except KeyboardInterrupt:
        pass
