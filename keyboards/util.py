from aiogram.types import ReplyKeyboardRemove
from aiogram.filters.callback_data import CallbackData

rkm = ReplyKeyboardRemove()


class PaginatorMammoths(CallbackData, prefix="pеg"):
    action: str
    page: int

