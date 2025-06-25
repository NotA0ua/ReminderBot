from datetime import datetime, timedelta

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Reminders


class RemindersOperations:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_reminder(
        self,
        user_id: int,
        name: str,
        repeat_interval: int,
        description: str | None = None,
        trigger_time: datetime | None = None,
    ) -> Reminders:
        reminder = Reminders(
            user_id=user_id,
            name=name,
            repeat_interval=repeat_interval,
            description=description,
            trigger_time=trigger_time,
        )

        self.session.add(reminder)

        return reminder

    async def get_reminder(self, reminder_id: int) -> Reminders | None:
        result = await self.session.execute(select(Reminders).filter_by(id=reminder_id))
        return result.scalar_one_or_none()

    async def get_user_reminders(self, user_id: int) -> list[Reminders]:
        result = await self.session.execute(
            select(Reminders).filter_by(user_id=user_id)
        )
        return list(result.scalars().all())

    async def update_reminder_trigger_time(self, reminder_id: int) -> Reminders | None:
        reminder = await self.session.get(Reminders, reminder_id)
        if reminder and reminder.repeat_interval:
            reminder.trigger_time += timedelta(seconds=float(reminder.repeat_interval))
            return reminder

        return None

    async def update_repeat_interval(
        self, reminder_id: int, repeat_interval: int
    ) -> Reminders | None:
        result = await self.session.execute(
            update(Reminders)
            .where(Reminders.id == reminder_id)
            .values(repeat_interval=repeat_interval)
            .returning(Reminders)
        )
        return result.scalar_one_or_none()

    async def update_active(self, reminder_id: int) -> Reminders | None:
        reminder = await self.session.get(Reminders, reminder_id)
        result = await self.session.execute(
            update(Reminders)
            .where(Reminders.id == reminder_id)
            .values(active=reminder.active)
            .returning(Reminders)
        )
        return result.scalar_one_or_none()

    async def update_description(
        self, reminder_id: int, description: str
    ) -> Reminders | None:
        result = await self.session.execute(
            update(Reminders)
            .where(Reminders.id == reminder_id)
            .values(description=description)
            .returning(Reminders)
        )
        return result.scalar_one_or_none()

    async def delete_reminder(self, reminder_id: int) -> bool:
        result = await self.session.execute(
            delete(Reminders).where(Reminders.id == reminder_id)
        )
        return result.rowcount > 0
