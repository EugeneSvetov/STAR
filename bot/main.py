from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.filters import register_all_filters
from bot.misc import TgKeys
import logging
from bot.handlers.other import scheduler
from bot.handlers import register_all_handlers
from bot.database.models import register_models
import os
from dotenv import load_dotenv

load_dotenv()

ADMINS = eval(os.getenv('ADMINS'))


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)
    await register_models()
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Я проснулась ☺️ Можно написать /start ")
        except Exception as err:
            logging.exception(err)


def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
