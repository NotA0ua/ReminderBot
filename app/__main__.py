import asyncio
import logging
import sys
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app import BOT_TOKEN
from app.database import Database
from app.handlers import setup_routers
from app.middlewares.database import DatabaseMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.middlewares.user import UserMiddleware
from app.utils.manager import UserManager

bot = Bot(
    token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)

db = Database()
dp = Dispatcher()

async def on_startup() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    await bot(DeleteWebhook(drop_pending_updates=True))

    await db.init_db()

    router = setup_routers()
    dp.include_router(router)

    # Middlewares
    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="app/locales/{locale}/LC_MESSAGES"),
        manager=UserManager(),
        default_locale="en",
    )

    dp.update.outer_middleware(DatabaseMiddleware(db))
    dp.update.outer_middleware(UserMiddleware(i18n_middleware))

    i18n_middleware.setup(dispatcher=dp)


    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

async def on_shutdown() -> None:
    await db.dispose()

async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
