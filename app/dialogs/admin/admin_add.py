from typing import Any

from aiogram import types, Bot
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Format

from app.database import AdminsOperations, UsersOperations
from app.states import AdminAdd
from app.dialogs import I18NFormat, button_close


async def admin_add_id_error(
    message: types.Message, _dialog: Any, manager: DialogManager, _error: ValueError
):
    i18n = manager.middleware_data["i18n"]
    await message.answer(i18n.get("admin_add_type_error"))


async def on_success(
    message: types.Message,
    _widget: ManagedTextInput[int],
    manager: DialogManager,
    data: int,
):
    session = manager.middleware_data["session"]
    i18n = manager.middleware_data["i18n"]
    admins = AdminsOperations(session)

    if not await UsersOperations(session, data).get_user():
        await message.answer(i18n.get("admin_add_user_error"))
    elif await admins.get_admin(data):
        await message.answer(i18n.get("admin_add_admin_error"))
    else:
        await admins.create_admin(data)
        await manager.next()


async def success_getter(bot: Bot, dialog_manager: DialogManager, **kwargs):
    admin_id = dialog_manager.find("admin_id").get_value()
    admin = await bot.get_chat_member(admin_id, admin_id)

    username = admin.user.username

    return {"admin_id": admin_id, "username": f"@{username} - " if username else ""}


dialog = Dialog(
    Window(
        I18NFormat("admin_add_message"),
        TextInput(
            id="admin_id",
            on_success=on_success,
            type_factory=int,
            on_error=admin_add_id_error,
        ),
        button_close,
        state=AdminAdd.id,
    ),
    Window(
        I18NFormat("admin_add_success_message"),
        Format("{username}`{admin_id}`"),
        button_close,
        state=AdminAdd.success,
        getter=success_getter,
    ),
)
