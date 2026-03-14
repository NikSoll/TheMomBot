import asyncio
import logging
from max_sdk import MaxBot
from config1 import MAX_KEY, BOT_ID, WEBHOOK_URL, SECRET_KEY
from handlers1 import register_handlers

logging.basicConfig(level=logging.INFO)


async def main():
    bot = MaxBot(
        api_key=MAX_KEY,
        bot_id=BOT_ID,
        secret_key=SECRET_KEY
    )

    register_handlers(bot)

    await bot.start_webhook(
        webhook_url=WEBHOOK_URL,
        port=5000
    )

    logging.info("✅ Max бот для записи запущен!")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())