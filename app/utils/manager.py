from aiogram import types
from aiogram_i18n.managers import BaseManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import UserOperations


class UserManager(BaseManager):
    async def set_locale(self, locale: str, session: AsyncSession, event_from_user: types.User) -> None:
        await UserOperations(session, event_from_user.id).update_language(locale)

    async def get_locale(self, session: AsyncSession, event_from_user: types.User) -> str:
        user = await UserOperations(session, event_from_user.id).get_user()
        return user.locale
