import asyncio
import uuid
from yookassa import Payment, Configuration
from django.conf import settings
from asgiref.sync import sync_to_async

Configuration.configure(settings.SHOP_ID_YOOKASSA, settings.SECRET_KEY_YOOKASSA)


async def create_payment(cart_id: int, amount: float) -> Payment:
    payment_id = f"cart-{cart_id}"
    description = f"Оплата заказа № {payment_id}"
    payment = await sync_to_async(Payment.create)(
        {
            "amount": {"value": amount, "currency": "RUB"},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {
                "type": "redirect",
                "return_url": settings.REDIRECT_URL,
            },
            "capture": True,
            "description": description,
        },
        uuid.uuid4(),
    )
    return payment


async def wait_for_payment_confirmation(payment_id: int) -> bool | None:
    while True:
        payment = await sync_to_async(Payment.find_one)(payment_id)
        if payment.status == "succeeded":
            return True
        elif payment == "canceled":
            return False
        await asyncio.sleep(3)
