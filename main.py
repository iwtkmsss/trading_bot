import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher

from third_bot.handlers.user import user_callback, user_message, user_command
from third_bot.handlers.worker import worker_callback, worker_handler, worker_command
from third_bot.misc import TOKEN


async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        worker_command.router,
        worker_callback.router,
        worker_handler.router,
        user_command.router,
        user_callback.router,
        user_message.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[-] BOT HAS BEEN DISABLE")
