import os
import django
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor
from bot.tg_bot.handlers import start_handler

# настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bottec_test.settings")
django.setup()


from django.conf import settings

# инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# регистрация хэндлеров и настроек диспетчера

dp.register_message_handler(start_handler, Command("start"))

# запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
