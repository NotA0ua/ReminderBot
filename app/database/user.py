import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserOperations:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def create_user(self, locale: str) -> User:
        user = User(id=self.user_id, locale=locale)
        self.session.add(user)

        logging.info(f"User has been created ({self.user_id} {locale})")

        return user

    async def get_user(self) -> User | None:
        result = await self.session.execute(select(User).filter_by(id=self.user_id))
        return result.scalar_one_or_none()

    async def update_language(self, locale: str) -> User | None:
        user = await self.get_user()
        user.locale = locale

        logging.info(f"User's language has been changed ({self.user_id} {locale})")

        return user
