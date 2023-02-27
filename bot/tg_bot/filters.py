from aiogram.types import CallbackQuery


async def catalog_filter(query: CallbackQuery):
    return query.data.startswith("catalog:")


async def menu_filter(query: CallbackQuery):
    return query.data == "menu"


async def subcategory_filter(query: CallbackQuery):
    return query.data.startswith("subcategory:")


async def products_filter(query: CallbackQuery):
    return query.data.startswith("product:")
