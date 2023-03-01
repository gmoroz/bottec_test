from aiogram.types import Message
from bot.tg_bot.channels import check_subscription
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


async def menu_handler(message: Message, check=True):
    """Хэндлер для обработки команды /menu и /start. Выводит меню, проверяет подписку"""
    if check:
        await check_subscription(message)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Каталог", callback_data="catalog:1"),
        InlineKeyboardButton("Корзина", callback_data="cart:1"),
        InlineKeyboardButton("FAQ", callback_data="faq:1"),
    )
    # Отправляем сообщение с InlineKeyboardMarkup пользователю
    await message.answer("Выберите действие:", reply_markup=keyboard)


async def menu_callback_handler(query: CallbackQuery):
    await menu_handler(query.message, check=False)
