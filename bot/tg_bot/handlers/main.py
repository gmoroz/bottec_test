from aiogram.types import Message
from bot.tg_bot.channels import check_subscription
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def menu_handler(message: Message):
    """Хэндлер для обработки команды /menu и /start. Выводит меню, проверяет подписку"""
    if await check_subscription(message):
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Каталог", callback_data="catalog"),
            InlineKeyboardButton("Корзина", callback_data="cart"),
            InlineKeyboardButton("FAQ", callback_data="faq"),
        )
        # Отправляем сообщение с InlineKeyboardMarkup пользователю
        await message.answer("Выберите действие:", reply_markup=keyboard)
