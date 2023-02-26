from start_bot import bot

async def check_subscription(channel_id: str, user_id: int) -> bool:
    """
    Проверка подписки пользователя на канал.
    """

    # Получаем информацию о пользователе.
    chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)

    # Проверяем, является ли пользователь участником канала и подписан ли он на него.
    return (
        chat_member.is_member and not chat_member.is_kicked and not chat_member.is_left
    )
