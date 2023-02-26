from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from aiogram.dispatcher import FSMContext
from bot.tg_bot.utils.db_queries import paginate, get_categories
from bot.tg_bot.handlers.sub_categories import sub_category_handler
from asgiref.sync import sync_to_async


def catalog_filter(c):
    return c.data.startswith("catalog:")


async def catalog_callback_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[1])
    await catalog_handler(query, page)


async def category_callback_handler(query: CallbackQuery, state: FSMContext):
    category_id = int(query.data.split(":")[1])
    page = 1
    await sub_category_handler(query, category_id, page)


async def catalog_handler(query: CallbackQuery, page: int = 1):
    """
    Хендлер для кнопки "Каталог".
    Выводит категории товаров в виде инлайн кнопок с пагинацией.
    """
    # Получаем кверисет категорий с пагинацией
    categories = await get_categories()
    categories_qs = await paginate(page, settings.CATEGORY_PAGE_SIZE, categories)

    # Создаем инлайн клавиатуру с кнопками-категориями
    keyboard = InlineKeyboardMarkup(row_width=1)
    async for category in categories_qs:
        button = InlineKeyboardButton(
            category.name, callback_data=f"category:{category.id}"
        )
        keyboard.insert(button)

    categories_count = await sync_to_async(categories.count)()
    # Добавляем кнопки переключения страниц
    total_pages = (categories_count + 1) // settings.CATEGORY_PAGE_SIZE
    if total_pages > 1:
        if page > 1:
            prev_button = InlineKeyboardButton(
                "◀️ Назад", callback_data=f"catalog:{page-1}"
            )
            keyboard.insert(prev_button)
        if page < total_pages:
            next_button = InlineKeyboardButton(
                "Вперед ▶️", callback_data=f"catalog:{page+1}"
            )
            keyboard.insert(next_button)

    menu_button = InlineKeyboardButton("Главное меню", callback_data="menu")
    keyboard.add(menu_button)

    # Отправляем сообщение с инлайн клавиатурой
    await query.message.edit_reply_markup(reply_markup=keyboard)
