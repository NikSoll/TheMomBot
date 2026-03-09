import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import redis

from config5 import BOT_TOKEN
from handlers5 import register_handlers

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    redis_client = redis.from_url("redis://localhost:6379/0")
    storage = RedisStorage(redis_client)
    dp = Dispatcher(storage=storage)

    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())