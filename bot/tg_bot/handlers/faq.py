from bot.models import FAQ
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from bot.tg_bot.utils.db_queries import paginate_qs
from asgiref.sync import sync_to_async
from bot.tg_bot.utils.keyboards import get_buttons



async def faq_handler(query: CallbackQuery):
    page = int(query.data.split(":")[1])
    faqs = await sync_to_async(FAQ.objects.order_by)("id")
    faq_qs = await paginate_qs(page, settings.QUESTIONS_ON_PAGE, faqs)

    keyboard = InlineKeyboardMarkup(row_width=1)
    async for faq in faq_qs:
        button = InlineKeyboardButton(
            faq.question, callback_data=f"question:{faq.id}:{page}"
        )
        keyboard.insert(button)
    faqs_count = await faqs.acount()
    total_pages = (faqs_count + faqs_count % 2) // settings.QUESTIONS_ON_PAGE
    buttons = await get_buttons(page, total_pages, "faq")
    keyboard.add(*buttons)
    await query.message.edit_text(reply_markup=keyboard, text="Выберите вопрос")


async def show_question(query: CallbackQuery):
    faq_id, back_page = map(int, query.data.split(":")[1:])
    faq = await FAQ.objects.aget(pk=faq_id)
    message = f"Q: {faq.question}\nA: {faq.answer}"

    back_button = InlineKeyboardButton("Назад", callback_data=f"faq:{back_page}")
    menu_button = InlineKeyboardButton("Главное меню", callback_data="menu")
    keyboard = InlineKeyboardMarkup(row_width=2).add(back_button, menu_button)

    await query.message.edit_text(reply_markup=keyboard, text=message)
