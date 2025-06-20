import logging

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Admin


class AdminOperations:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_admin(self, user_id: int) -> Admin:
        user = Admin(id=user_id)
        self.session.add(user)

        logging.info(f"Admin has been created ({user_id})")

        return user

    async def get_admin(self, user_id: int) -> Admin | None:
        result = await self.session.execute(select(Admin).filter_by(id=user_id))
        return result.scalar_one_or_none()

    async def get_all_admins(self) -> list[Admin]:
        result = await self.session.execute(select(Admin))
        return list(result.scalars().all())

    async def delete_admin(self, user_id: int) -> bool:
        result = await self.session.execute(delete(Admin).where(Admin.id == user_id))
        return result.rowcount > 0
