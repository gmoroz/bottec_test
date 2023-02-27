from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InlineKeyboardButton,
)
from django.conf import settings
from bot.models import Subcategory
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
from bot.tg_bot.utils.keyboards import get_buttons
from aiogram.types.input_file import InputFile


async def product_callback_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[2])
    await products_handler(query, page)


async def products_handler(query: CallbackQuery, page: int = 1):
    subcategory_id = int(query.data.split(":")[1])
    subcategory = await Subcategory.objects.aget(pk=subcategory_id)
    products = subcategory.products.order_by("pk").all()

    keyboard = InlineKeyboardMarkup(row_width=2)

    products_count = await sync_to_async(products.count)()
    total_pages = (
        products_count + int(settings.PRODUCTS_ITEMS_ON_PAGE > 1)
    ) // settings.PRODUCTS_ITEMS_ON_PAGE
    product = await sync_to_async(products.__getitem__)(page - 1)
    cart_button = InlineKeyboardButton(
        "Добавить в корзину", callback_data=f"cart_add:{product.id}:1:process"
    )
    butttons = await get_buttons(
        page, total_pages, callback_data=f"product:{subcategory_id}"
    ) + [cart_button]
    keyboard.add(*butttons)
    if query.message.photo:
        await query.bot.edit_message_media(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            media=InputMediaPhoto(
                media=InputFile(product.image.path),
                caption=await product.caption(),
            ),
            reply_markup=keyboard,
        )
    else:
        await query.bot.send_photo(
            chat_id=query.message.chat.id,
            photo=InputFile(product.image.path),
            caption=await product.caption(),
            reply_markup=keyboard,
        )
