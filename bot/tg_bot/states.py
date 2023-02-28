from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    waiting_for_address = State()
    waiting_for_address_confirmation = State()
