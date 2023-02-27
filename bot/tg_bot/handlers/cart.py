from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from bot.tg_bot.utils.keyboards import get_quantity_keyboard


async def process_cart_add(query: CallbackQuery, state: FSMContext):
    _, product_id, quantity, action = query.data.split(":")
    user_id = query.from_user.id
    await state.update_data(product_id=product_id)
    quantity = int(quantity)

    match action:
        case "increment":
            quantity = quantity + 1
        case "decrement":
            quantity = quantity - 1 if quantity > 1 else quantity

    keyboard = await get_quantity_keyboard(int(product_id), quantity)
    text = f"Текущее количество: {quantity}\nУкажите количество или подтвердите покупку"
    if query.message.photo:
        await query.bot.send_message(user_id, text, reply_markup=keyboard)
    else:
        try:
            await query.message.edit_text(text, reply_markup=keyboard)
        except MessageNotModified:
            pass
