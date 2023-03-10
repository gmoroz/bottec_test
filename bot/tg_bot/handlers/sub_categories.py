from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from bot.tg_bot.utils.db_queries import paginate_qs
from bot.models import Category
from aiogram.dispatcher import FSMContext

from bot.tg_bot.utils.keyboards import get_buttons


async def subcategory_callback_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[2])
    await subcategories_handler(query, page)


async def subcategories_handler(query: CallbackQuery, page: int = 1):
    category_id = int(query.data.split(":")[1])
    category = await Category.objects.aget(pk=category_id)
    subcategories = category.subcategories.all()
    subcategories_qs = await paginate_qs(
        page, settings.SUBCATEGORY_ITEMS_ON_PAGE, subcategories
    )

    keyboard = InlineKeyboardMarkup(row_width=1)
    async for subcategory in subcategories_qs:
        button = InlineKeyboardButton(
            subcategory.name, callback_data=f"product:{subcategory.id}:1"
        )
        keyboard.insert(button)
    subcategories_count = await subcategories.acount()

    # Добавляем кнопки переключения страниц
    total_pages = (subcategories_count + 1) // settings.SUBCATEGORY_ITEMS_ON_PAGE
    back_button = InlineKeyboardButton("Назад к категориям", callback_data="catalog:1")
    buttons = await get_buttons(page, total_pages, f"subcategory:{category_id}")
    buttons.insert(-1, back_button)
    keyboard.add(*buttons)

    await query.message.edit_reply_markup(reply_markup=keyboard)
