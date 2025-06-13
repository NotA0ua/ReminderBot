from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserOperations:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_id: int) -> User:
        user = User(id=user_id)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalar_one_or_none()

    async def update_language(self, user_id: int, language: str) -> User | None:
        user = await self.get_user(user_id)
        user.language = language
        await self.session.flush()
        return user
