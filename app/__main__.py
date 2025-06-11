import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook

dp = Dispatcher()
dp.include_routers(router)

dp.message.middleware(ThrottlingMiddleware())
dp.callback_query.middleware(ThrottlingMiddleware())


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    await bot(DeleteWebhook(drop_pending_updates=True))

    await dp.start_polling(bot)
