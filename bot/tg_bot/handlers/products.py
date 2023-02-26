from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from bot.tg_bot.utils.db_queries import paginate_qs
from bot.models import Subcategory
from aiogram.dispatcher import FSMContext

from bot.tg_bot.utils.paginate import get_buttons


async def product_callback_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[2])
    await products_handler(query, page)


async def products_handler(query: CallbackQuery, page: int = 1):
    subcategory_id = int(query.data.split(":")[1])
    subcategory = await Subcategory.objects.aget(pk=subcategory_id)
    products = subcategory.products.all()
    products_qs = await paginate_qs(page, settings.PRODUCTS_PAGE_SIZE, products)

    InlineKeyboardMarkup(row_width=2)
    async for product in products_qs:
        InlineKeyboardButton()
    total_pages = settings.CATEGORY_PAGE_SIZE
    await get_buttons(page, total_pages, callback_data=f"cart:{product.id}:1")
