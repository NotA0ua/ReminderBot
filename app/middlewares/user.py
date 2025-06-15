import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram_i18n import I18nMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Database, UserOperations


class UserMiddleware(BaseMiddleware):
    def __init__(self, i18n_middleware: I18nMiddleware):
        self.i18n_middleware = i18n_middleware

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_user: types.User = data["event_from_user"]
        session: AsyncSession = data["session"]

        user_operations = UserOperations(session=session)

        user = await user_operations.get_user(user_id=event_user.id)
        if not user:
            user_language = event_user.language_code

            if user_language not in self.i18n_middleware.core.available_locales:
                user_language = self.i18n_middleware.core.default_locale

            await user_operations.create_user(
                user_id=event_user.id,
                locale=user_language,
            )

        return await handler(event, data)
