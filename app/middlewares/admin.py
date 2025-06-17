from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware, types

from app.database import AdminOperations


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session = data["session"]
        admin = AdminOperations(session)
        event_user: types.User = data["event_from_user"]
        if await admin.get_admin(event_user.id):
            return await handler(event, data)
        else:
            return None
