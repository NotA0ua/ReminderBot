import logging
from typing import Any

from aiogram import Router, types
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Next, Button
from aiogram_i18n import LazyFilter, I18nContext

from app.states import AdminAdd
from app.utils import I18NFormat

router = Router()

async def admin_add_id_error(message: types.Message, dialog_: Any, manager: DialogManager, error_: ValueError):
    i18n = manager.middleware_data["i18n"]
    await message.answer(i18n.get("admin_add_error"))


dialog = Dialog(
    Window(
        I18NFormat("admin_add_message"),
        TextInput(id="country", on_success=Next(), type_factory=int, on_error=admin_add_id_error),
        Button(I18NFormat("close"), id="admin_add_close"),
        state=AdminAdd.id,
    ),
    Window(
        Format(""),
        Button(I18NFormat("close"), id="admin_add_close"),
        state=AdminAdd.success,
    ),
)

router.include_router(dialog)

@router.message(LazyFilter("admin_add_handler"))
async def admin_add_handler(message_: types.Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(AdminAdd.id, mode=StartMode.RESET_STACK)
