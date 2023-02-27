from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from aiogram.dispatcher import FSMContext
from bot.tg_bot.utils.db_queries import paginate_qs, get_categories
from bot.tg_bot.handlers.sub_categories import subcategories_handler

from bot.tg_bot.utils.keyboards import get_buttons


async def catalog_callback_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[1])
    await catalog_handler(query, page)


async def category_callback_handler(query: CallbackQuery, state: FSMContext):
    await subcategories_handler(query)


async def catalog_handler(query: CallbackQuery, page: int = 1):
    """
    Хендлер для кнопки "Каталог".
    Выводит категории товаров в виде инлайн кнопок с пагинацией.
    """
    # Получаем кверисет категорий с пагинацией
    categories = await get_categories()
    categories_qs = await paginate_qs(page, settings.CATEGORY_ITEMS_ON_PAGE, categories)

    # Создаем инлайн клавиатуру с кнопками-категориями
    keyboard = InlineKeyboardMarkup(row_width=1)
    async for category in categories_qs:
        button = InlineKeyboardButton(
            category.name, callback_data=f"subcategory:{category.id}:1"
        )
        keyboard.insert(button)

    categories_count = await categories.acount()
    # Добавляем кнопки переключения страниц
    total_pages = (categories_count + 1) // settings.CATEGORY_ITEMS_ON_PAGE
    buttons = await get_buttons(page, total_pages, "catalog")
    keyboard.add(*buttons)

    # Отправляем сообщение с инлайн клавиатурой
    await query.message.edit_reply_markup(reply_markup=keyboard)
