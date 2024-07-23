from aiogram.filters import BaseFilter
from aiogram.types import (Message, CallbackQuery)


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message | CallbackQuery, admin_ids: list[int]) -> bool:
        return message.from_user.id in admin_ids
