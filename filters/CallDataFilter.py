from aiogram.filters import Filter
from aiogram.types import CallbackQuery


class CallData(Filter):
    def __init__(self, callback_data):
        self.callback_data = callback_data

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        if self.callback_data == callback_query.data.split("_")[0]:
            return True
        return False
