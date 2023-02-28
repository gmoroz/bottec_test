from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.utils.callback_data import CallbackData

from bot.tg_bot.states import OrderState
from bot.tg_bot.utils.keyboards import get_address_confirm_keyboard

shipping_callback = CallbackData("shipping", "action")


async def ask_address(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пожалуйста, введите ваш адрес для доставки")
    await OrderState.waiting_for_address.set()


async def receive_address(message: Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)

    keyboard = await get_address_confirm_keyboard(shipping_callback)
    await message.answer(
        f"Ваш адрес доставки: {address}\n\nПодтвердите, что это правильный адрес:",
        reply_markup=keyboard,
    )
    await OrderState.waiting_for_address_confirmation.set()


async def confirm_address(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address = data.get("address")

    # TODO: Платежка тинькофф / фрикасса
    await call.message.answer(f"Заказ оформлен на адрес {address}")

    await state.finish()


async def edit_address(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пожалуйста, введите ваш адрес для доставки")
    await OrderState.waiting_for_address.set()
