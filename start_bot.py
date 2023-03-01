import os
import django
from aiogram.dispatcher.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor
from bot.tg_bot import filters as f


# настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bottec_test.settings")
django.setup()


from django.conf import settings
from bot.tg_bot.handlers.categories import catalog_callback_handler
from bot.tg_bot.handlers.sub_categories import subcategory_callback_handler
from bot.tg_bot.handlers.products import product_callback_handler
from bot.tg_bot.handlers import cart as c
from bot.tg_bot.handlers.main import menu_callback_handler, menu_handler
from bot.tg_bot.handlers import shipping as s
from bot.tg_bot.states import OrderState

# инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
order_state = OrderState()

# регистрация хэндлеров и настроек диспетчера

dp.register_message_handler(menu_handler, Command(["menu", "start"]))
dp.register_callback_query_handler(menu_callback_handler, f.menu_filter)

dp.register_callback_query_handler(catalog_callback_handler, f.catalog_filter)

dp.register_callback_query_handler(subcategory_callback_handler, f.subcategory_filter)

dp.register_callback_query_handler(product_callback_handler, f.products_filter)

dp.register_callback_query_handler(c.process_cart_add, f.cart_quantity_filter)
dp.register_callback_query_handler(
    c.cart_ask_confirmation_callback, f.cart_confirm_filter
)

dp.register_callback_query_handler(
    c.add_product_to_cart,
    f.add_product_to_cart_filter,
)
dp.register_callback_query_handler(
    c.cart_show,
    f.cart_show_filter,
)
dp.register_callback_query_handler(
    c.cart_delete_product,
    f.cart_delete_product_filter,
)
dp.register_callback_query_handler(c.add_product_to_cart, state=order_state)
dp.register_callback_query_handler(c.cart_show, state=order_state)
dp.register_callback_query_handler(c.cart_delete_product, state=order_state)

dp.register_callback_query_handler(
    s.ask_address, s.shipping_callback.filter(action="ask_address")
)
dp.register_callback_query_handler(
    s.receive_address, s.shipping_callback.filter(action="receive_address")
)
dp.register_callback_query_handler(
    s.confirm_address, s.shipping_callback.filter(action="confirm")
)
dp.register_callback_query_handler(
    s.edit_address,
    s.shipping_callback.filter(action="edit"),
)

dp.register_message_handler(s.receive_address, state=OrderState.waiting_for_address)
dp.register_callback_query_handler(
    s.confirm_address, state=OrderState.waiting_for_address_confirmation
)
dp.register_callback_query_handler(
    s.edit_address, state=OrderState.waiting_for_address_confirmation
)

# запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
