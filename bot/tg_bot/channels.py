from aiogram.utils.exceptions import TelegramAPIError

from django.conf import settings


async def check_subscription(user_id: int):
    from start_bot import bot

    try:
        chat_member = await bot.get_chat_member(
            chat_id=settings.CHANNEL_ID, user_id=user_id
        )
        return chat_member.is_chat_member()
    except TelegramAPIError:
        return False
