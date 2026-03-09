import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import redis

from config2 import SHOP_SETTINGS
from handlers2 import register_handlers

logging.basicConfig(level=logging.INFO)

TOKEN = "sdvsdvsdvsdvsdv"


async def main():
    bot = Bot(token=TOKEN)
    redis_client = redis.from_url("redis://localhost:6379/0")
    storage = RedisStorage(redis_client)
    dp = Dispatcher(storage=storage)

    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())