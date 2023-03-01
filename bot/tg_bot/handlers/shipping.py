from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.utils.callback_data import CallbackData
from bot.models import Cart
from bot.tg_bot.handlers.main import menu_callback_handler
from bot.tg_bot.utils.excel_write import save_order_data_to_excel
from bot.tg_bot.utils.payments import create_payment, wait_for_payment_confirmation

from bot.tg_bot.states import OrderState
from bot.tg_bot.utils.keyboards import get_address_confirm_keyboard

shipping_callback = CallbackData("shipping", "action")


async def ask_address(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пожалуйста, введите ваш адрес для доставки")
    await OrderState.waiting_for_address.set()


async def receive_address(message: Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address, username=message.from_user.username)

    data = await state.get_data()
    amount = data.get("amount")
    cart_id = data.get("cart_id")
    cart = (
        await Cart.objects.filter(pk=cart_id)
        .prefetch_related("products__product")
        .afirst()
    )
    products = []
    async for cart_product in cart.products.all():
        product_string = f"{cart_product.product.name}: {cart_product.quantity} шт."
        products.append(product_string)
    products.append(f"Общая стоимость: {amount}")
    products_string = "\n".join(products)

    keyboard = await get_address_confirm_keyboard(shipping_callback)
    await message.answer(
        f"Ваши товары: {products_string}\nВаш адрес доставки: {address}\n"
        "\nПодтвердите, что это правильный адрес",
        reply_markup=keyboard,
    )
    await OrderState.waiting_for_address_confirmation.set()


async def confirm_address(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address = data.get("address")
    cart_id = data.get("cart_id")
    payment_amount = data.get("amount")
    payment = await create_payment(cart_id, payment_amount)
    payment_id = payment.id
    payment_url = payment.confirmation.confirmation_url

    await query.message.answer(
        f"Для оплаты заказа на адрес `{address}` перейдите по ссылке: {payment_url}"
    )

    payment_status = await wait_for_payment_confirmation(payment_id)

    if payment_status:
        username = data.get("username")
        cart = (
            await Cart.objects.filter(pk=cart_id)
            .prefetch_related("products__product")
            .afirst()
        )
        products = []
        async for cart_product in cart.products.all():
            products.append((cart_product.product.name, cart_product.quantity))
        data = {
            "username": username,
            "products": products,
            "payment_amount": payment_amount,
            "payment_id": payment_id,
            "address": address,
        }

        await Cart.objects.filter(pk=cart_id).adelete()
        await save_order_data_to_excel(data)
        await query.message.answer(
            f"Оплата прошла успешно. Ваш заказ оформлен адрес `{address}`"
        )
    else:
        await query.message.answer("Оплата не удалась. Попробуйте еще раз.")

    await state.finish()
    await menu_callback_handler(query)


async def edit_address(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пожалуйста, введите ваш адрес для доставки")
    await OrderState.waiting_for_address.set()
