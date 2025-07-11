from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram_i18n import I18nMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import UsersOperations


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

        user_operations = UsersOperations(session=session, user_id=event_user.id)

        user = await user_operations.get_user()
        if not user:
            user_locale = event_user.language_code

            if user_locale not in self.i18n_middleware.core.available_locales:
                user_locale = self.i18n_middleware.core.default_locale

            await user_operations.create_user(locale=user_locale)

        return await handler(event, data)
