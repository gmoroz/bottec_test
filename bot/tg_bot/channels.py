from aiogram.utils.exceptions import TelegramAPIError
from aiogram.types import Message
from django.conf import settings

from bot.models import User


async def check_subscription(message: Message):
    from start_bot import bot

    try:
        await bot.get_chat_member(
            chat_id=settings.CHANNEL_ID, user_id=message.from_user.id
        )
        tg_id = message.from_user.id
        user_channel_status = await bot.get_chat_member(
            chat_id=settings.CHANNEL_ID, user_id=tg_id
        )
        username = message.from_user.username
        if user_channel_status["status"] != "left":
            await User.objects.aget_or_create(username=username, tg_id=tg_id)
            return True
        else:
            await message.answer(f"Вы не подписаны на канал {settings.CHANNEL_ID}")
    except TelegramAPIError:
        await message.answer(f"Вы не подписаны на канал {settings.CHANNEL_ID}")
