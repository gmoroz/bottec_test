from aiogram.utils.exceptions import TelegramAPIError
from aiogram.types import Message
from django.conf import settings


async def check_subscription(message: Message):
    from start_bot import bot

    try:
        chat_member = await bot.get_chat_member(
            chat_id=settings.CHANNEL_ID, user_id=message.from_user.id
        )
        return chat_member.is_chat_member()
    except TelegramAPIError:
        await message.answer("Вы не подписаны на канал {settings.CHANNEL_ID}")
