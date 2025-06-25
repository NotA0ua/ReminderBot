from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode
from aiogram_i18n import LazyFilter, I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.dialogs.admin import dialogs
from app.handlers.user.start import start_handler
from app.states import Admins, AdminAdd
from app.utils import admin_commands_keyboard

router = Router()

router.include_routers(*dialogs())


@router.message(LazyFilter("admin_handler"))
async def admin_handler(message: types.Message, i18n: I18nContext) -> None:
    await message.answer(
        i18n.get("admin_message"), reply_markup=admin_commands_keyboard()
    )


@router.message(LazyFilter("admins_handler"))
async def admins_handler(
    _message: types.Message, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(Admins.admins, mode=StartMode.RESET_STACK)


@router.message(LazyFilter("admin_add_handler"))
async def admin_add_handler(
    _message: types.Message, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(AdminAdd.id, mode=StartMode.RESET_STACK)


@router.message(LazyFilter("admin_exit_handler"))
async def admin_handler(
    message: types.Message, i18n: I18nContext, session: AsyncSession
) -> None:
    await start_handler(message, i18n, session)
