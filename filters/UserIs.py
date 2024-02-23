from aiogram.filters import Filter
from aiogram.types import Message

from third_bot.misc import BDB


class UserWorker(Filter):
    async def __call__(self, message: Message) -> bool:
        users = await BDB.user_exists_main(message.from_user.id)
        if users:
            return True
        return False


class UserAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        for i in await BDB.get_all_admin():
            if message.from_user.id == i[0]:
                return True
        return False


class UserTp(Filter):
    async def __call__(self, message: Message) -> bool:
        for i in await BDB.get_all_admin():
            if message.from_user.id == i[0]:
                return True
        for i in await BDB.get_all_tp():
            if message.from_user.id == i[0]:
                return True
        return False
