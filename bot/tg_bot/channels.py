from aiogram.utils.exceptions import TelegramAPIError
from aiogram.types import Message
from django.conf import settings

from bot.models import User


async def check_subscription(message: Message):
    from start_bot import bot

    try:
        chat_member = await bot.get_chat_member(
            chat_id=settings.CHANNEL_ID, user_id=message.from_user.id
        )
        tg_id = message.from_user.id
        username = message.from_user.username
        if chat_member.is_chat_member():
            await User.objects.aget_or_create(username=username, tg_id=tg_id)
            return True
    except TelegramAPIError:
        await message.answer("Вы не подписаны на канал {settings.CHANNEL_ID}")
