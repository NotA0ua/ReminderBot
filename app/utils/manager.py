from aiogram import types
from aiogram_i18n.managers import BaseManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import UsersOperations


class UserManager(BaseManager):
    async def set_locale(
        self, locale: str, session: AsyncSession, event_from_user: types.User
    ) -> None:
        await UsersOperations(session, event_from_user.id).update_locale(locale)

    async def get_locale(
        self, session: AsyncSession, event_from_user: types.User
    ) -> str:
        user = await UsersOperations(session, event_from_user.id).get_user()
        return user.locale
