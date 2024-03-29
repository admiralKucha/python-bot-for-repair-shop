import asyncio
import logging
from aiogram import Bot, Dispatcher
from init import TOKEN
from handlers import registration, user, show_tables, auth, price, company, worker, customer

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def main():
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер
    dp = Dispatcher()

    dp.include_routers(registration.router,
                       user.router,
                       show_tables.router,
                       auth.router,
                       price.router,
                       company.router,
                       worker.router,
                       customer.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
