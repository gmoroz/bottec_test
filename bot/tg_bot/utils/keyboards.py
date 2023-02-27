from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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


async def get_quantity_keyboard(quantity: int = 1):
    plus_button = InlineKeyboardButton("+", callback_data="cart_quantity:increment")
    minus_button = InlineKeyboardButton("-", callback_data="cart_quantity:decrement")
    quantity_text = f"{quantity}"
    quantity_button = InlineKeyboardButton(
        quantity_text, callback_data="cart_quantity:show"
    )

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(minus_button, quantity_button, plus_button)

    return keyboard
