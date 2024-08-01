from aiogram.filters import BaseFilter
from aiogram.types import (Message, CallbackQuery)

from models.models import db


class SuperAdmin(BaseFilter):
    async def __call__(self, message: Message | CallbackQuery, admin_ids: list[int]) -> bool:
        return message.from_user.id in admin_ids


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message | CallbackQuery, admin_ids: list[int]) -> bool:
        data: list[tuple[int]] | None = await db.select_values(name_table='admins', columns=('user_id',))
        if data is not None:
            admins: list[int] = [admin[0] for admin in data]
            return message.from_user.id in admin_ids or message.from_user.id in admins
        return message.from_user.id in admin_ids
