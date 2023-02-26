import os
import django
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor
from bot.tg_bot.filters import catalog_filter, menu_filter, subcategory_filter

from bot.tg_bot.handlers.main import menu_callback_handler, menu_handler


# настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bottec_test.settings")
django.setup()


from django.conf import settings
from bot.tg_bot.handlers.categories import catalog_callback_handler
from bot.tg_bot.handlers.sub_categories import (
    subcategory_callback_handler,
)

# инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# регистрация хэндлеров и настроек диспетчера

dp.register_message_handler(menu_handler, Command(["menu", "start"]))
dp.register_callback_query_handler(menu_callback_handler, menu_filter)
dp.register_callback_query_handler(catalog_callback_handler, catalog_filter)
dp.register_callback_query_handler(subcategory_callback_handler, subcategory_filter)
# запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
