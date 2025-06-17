from aiogram import Router, types
from aiogram_i18n import LazyFilter, I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.user.start import start_handler
from app.utils import admin_commands_keyboard

router = Router()


@router.message(LazyFilter("admin_handler"))
async def admin_handler(message: types.Message, i18n: I18nContext) -> None:
    await message.answer(
        i18n.get("admin_message"), reply_markup=admin_commands_keyboard()
    )


@router.message(LazyFilter("admin_exit_handler"))
async def admin_handler(
    message: types.Message, i18n: I18nContext, session: AsyncSession
) -> None:
    await start_handler(message, i18n, session)
