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
from app.handlers import setup_routers
from app.middlewares.throttling import ThrottlingMiddleware


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    await bot(DeleteWebhook(drop_pending_updates=True))

    dp = Dispatcher()

    router = setup_routers()
    dp.include_router(router)

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="app/locales/{locale}/LC_MESSAGES")
    )

    i18n_middleware.setup(dispatcher=dp)
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
