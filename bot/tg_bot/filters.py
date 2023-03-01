from aiogram.types import CallbackQuery


async def catalog_filter(query: CallbackQuery):
    return query.data.startswith("catalog:")


async def menu_filter(query: CallbackQuery):
    return query.data == "menu"


async def subcategory_filter(query: CallbackQuery):
    return query.data.startswith("subcategory:")


async def products_filter(query: CallbackQuery):
    return query.data.startswith("product:")


async def cart_quantity_filter(query: CallbackQuery):
    return query.data.startswith("cart_add:")


async def cart_confirm_filter(query: CallbackQuery):
    return query.data.startswith("cart_confirm:")


async def add_product_to_cart_filter(query: CallbackQuery):
    return query.data.startswith("cart_update:")


async def cart_show_filter(query: CallbackQuery):
    return query.data.startswith("cart:")


async def cart_delete_product_filter(query: CallbackQuery):
    return query.data.startswith("delete:")


async def faq_filter(query: CallbackQuery):
    return query.data.startswith("faq:")


async def question_show_filter(query: CallbackQuery):
    return query.data.startswith("question:")
