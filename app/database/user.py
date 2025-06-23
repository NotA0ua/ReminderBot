import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Users


class UsersOperations:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def create_user(self, locale: str) -> Users | None:
        user = Users(id=self.user_id, locale=locale)
        self.session.add(user)

        logging.info(f"User has been created ({self.user_id} {locale})")

        return user

    async def get_user(self) -> Users | None:
        result = await self.session.execute(select(Users).filter_by(id=self.user_id))
        return result.scalar_one_or_none()

    async def update_locale(self, locale: str) -> Users | None:
        user = await self.get_user()
        user.locale = locale

        logging.info(f"User's locale has been changed ({self.user_id} {locale})")

        return user
