from aiogram.types import InlineKeyboardButton


async def get_buttons(
    page: int, total_pages: int, callback_data: str
) -> list[InlineKeyboardButton]:
    buttons: list[InlineKeyboardButton] = []
    if total_pages > 1:
        if page > 1:
            prev_button = InlineKeyboardButton(
                "◀️ Назад", callback_data=f"{callback_data}:{page-1}"
            )
            buttons.append(prev_button)
        if page < total_pages:
            next_button = InlineKeyboardButton(
                "Вперед ▶️", callback_data=f"{callback_data}:{page+1}"
            )
            buttons.append(next_button)
    menu_button = InlineKeyboardButton("Главное меню", callback_data="menu")
    return buttons + [menu_button]
