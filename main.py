import logging
from aiogram import Bot, Dispatcher
import asyncio
from config import settings
from handlers import router

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
