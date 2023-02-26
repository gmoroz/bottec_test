from aiogram.dispatcher.filters.state import State, StatesGroup


class CatalogState(StatesGroup):
    Category = State()
    Subcategory = State()
    Product = State()


class OrderState(StatesGroup):
    Shipping = State()
    Payment = State()


class FAQState(StatesGroup):
    Answer = State()
