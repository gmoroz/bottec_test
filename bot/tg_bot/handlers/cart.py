from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from bot.models import Cart, CartProduct, Product, User
from bot.tg_bot.handlers.main import menu_callback_handler
from bot.tg_bot.utils.db_queries import paginate_qs
from bot.tg_bot.utils.keyboards import get_buttons, get_quantity_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from aiogram.dispatcher import FSMContext
from bot.tg_bot.handlers.shipping import shipping_callback


async def process_cart_add(query: CallbackQuery):
    _, product_id, quantity, action = query.data.split(":")
    tg_id = query.from_user.id
    quantity, product_id = map(int, (quantity, product_id))
    cart = await Cart.objects.aget(user__tg_id=tg_id)
    product = await cart.products.filter(product_id=product_id).afirst()
    if product:
        await query.answer(text="Этот товар уже есть в вашей корзине!")
        await menu_callback_handler(query)

    match action:
        case "increment":
            quantity = quantity + 1
        case "decrement":
            quantity = quantity - 1 if quantity > 1 else quantity

    keyboard = await get_quantity_keyboard(product_id, quantity)
    text = f"Текущее количество: {quantity}\nУкажите количество или подтвердите покупку"
    if query.message.photo:
        await query.message.answer(text, reply_markup=keyboard)
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
        "Да, перейти в корзину", callback_data=f"cart_update:{product_id}:{quantity}"
    )
    back_button = InlineKeyboardButton(
        "Назад", callback_data=f"cart_add:{product_id}:{quantity}:process"
    )
    keyboard.add(ok_button, back_button)
    await query.message.edit_text(text, reply_markup=keyboard)


async def add_product_to_cart(query: CallbackQuery, state: FSMContext):
    product_id, quantity = map(int, query.data.split(":")[1:])

    tg_id = query.from_user.id
    cart = await Cart.objects.aget(user__tg_id=tg_id)
    product = await cart.products.filter(product_id=product_id).afirst()
    if product:
        await query.answer(text="Этот товар уже есть в вашей корзине!")
        return

    product = await Product.objects.aget(pk=product_id)
    tg_id = query.from_user.id
    user = await User.objects.aget(tg_id=tg_id)
    cart, _ = await Cart.objects.aget_or_create(user=user)
    await CartProduct.objects.acreate(
        cart=cart,
        product=product,
        quantity=quantity,
    )
    await cart_show(query, state, page=1)


async def cart_show(query: CallbackQuery, state: FSMContext, page: int | None = None):
    if page is None:
        page = int(query.data.split(":")[1])
    tg_id = query.from_user.id

    cart = (
        await Cart.objects.filter(user__tg_id=tg_id)
        .prefetch_related("products__product")
        .afirst()
    )
    cart_products = cart.products.all()
    products_count = await cart_products.acount()
    if products_count:
        products = []
        await state.update_data(cart_id=cart.id)
        keyboard = InlineKeyboardMarkup(row_width=1)
        cart_products_list = await paginate_qs(
            page, settings.PRODUCTS_IN_CART_COUNT, cart_products
        )
        amount = 0
        for cart_product in cart_products_list:
            amount += cart_product.quantity * cart_product.product.price
            name = cart_product.product.name
            product_string = f"{name}: {cart_product.quantity} шт."
            products.append(product_string)
            button = InlineKeyboardButton(
                f"удалить {name}...",
                callback_data=f"delete:{cart_product.product.id}:{cart.id}",
            )
            keyboard.insert(button)
        await state.update_data(amount=amount)
        products.append(f"Общая стоимость: {amount}₽")
        text = "\n".join(products)

        total_pages = (
            products_count + products_count % 2
        ) // settings.PRODUCTS_IN_CART_COUNT
        buttons = await get_buttons(page, total_pages, "cart")
        keyboard.add(*buttons)
        keyboard.add(
            InlineKeyboardButton(
                "Заказать доставку",
                callback_data=shipping_callback.new(action="ask_address"),
            )
        )
        message_text = query.message.text
        if "Вы хотите добавить в корзину товар" in message_text:
            await query.message.answer(text=text, reply_markup=keyboard)
        else:
            await query.message.edit_text(text=text, reply_markup=keyboard)
    else:
        await query.answer("Ваша корзина пуста!")
        return


async def cart_delete_product(query: CallbackQuery, state: FSMContext):
    product_id, cart_id = map(int, query.data.split(":")[1:])
    await CartProduct.objects.filter(cart_id=cart_id, product_id=product_id).adelete()
    await query.answer("Товар успешно удален из корзины!")
    query.data = "cart:1"
    await cart_show(query, state)
