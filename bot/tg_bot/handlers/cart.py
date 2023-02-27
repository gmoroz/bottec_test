from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from bot.models import Cart, CartProduct, Product, User
from bot.tg_bot.utils.keyboards import get_quantity_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def process_cart_add(query: CallbackQuery):
    _, product_id, quantity, action = query.data.split(":")
    user_id = query.from_user.id
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


async def cart_ask_confirmation_callback(query: CallbackQuery):
    product_id, quantity = map(int, query.data.split(":")[1:])
    product = await Product.objects.aget(pk=product_id)
    text = f"Вы хотите добавить в корзину товар '{product.name}'\n цена за шт: {product.price}₽"
    if quantity > 1:
        text += f"\n цена за {quantity} шт: {quantity * product.price}₽"
    keyboard = InlineKeyboardMarkup(row_width=2)
    ok_button = InlineKeyboardButton(
        "Перейти в корзину", callback_data=f"cart_update:{product_id}:{quantity}"
    )
    back_button = InlineKeyboardButton(
        "Назад", callback_data=f"cart_add:{product_id}:{quantity}:process"
    )
    keyboard.add(ok_button, back_button)
    await query.message.edit_text(text, reply_markup=keyboard)


async def add_product_to_cart(query: CallbackQuery):
    product_id, quantity = map(int, query.data.split(":")[1:])
    product = await Product.objects.aget(pk=product_id)
    tg_id = query.from_user.id
    user = await User.objects.aget(tg_id=tg_id)
    cart, _ = await Cart.objects.aget_or_create(user=user)
    await CartProduct.objects.acreate(
        cart=cart,
        product=product,
        quantity=quantity,
    )
    await cart_show(query)


async def cart_show(query: CallbackQuery):
    pass
