from aiogram.types import Message
from bot.tg_bot.channels import check_subscription
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def start_handler(message: Message):
    """Хэндлер для обработки команды /start. Проверяет подписку пользователя на канал."""
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer("Вы уже подписаны на канал!")
    else:
        await message.answer("Вы не подписаны на канал!")


async def menu_handler(message: Message):
    if await check_subscription(message.from_user.id):
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Каталог", callback_data="catalog"),
            InlineKeyboardButton("Корзина", callback_data="cart"),
            InlineKeyboardButton("FAQ", callback_data="faq"),
        )
        # Отправляем сообщение с InlineKeyboardMarkup пользователю
        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        await message.answer("Вы не подписаны на канал!")
