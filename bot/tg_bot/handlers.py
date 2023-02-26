from aiogram.types import Message
from bot.tg_bot.channels import check_subscription


async def start_handler(message: Message):
    """Хэндлер для обработки команды /start. Проверяет подписку пользователя на канал."""
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer("Вы уже подписаны на канал!")
    else:
        await message.answer("Вы не подписаны на канал!")
