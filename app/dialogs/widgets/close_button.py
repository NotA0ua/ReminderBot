from aiogram import types
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from . import I18NFormat


async def dialog_close(
    callback: types.CallbackQuery, _button: Button, manager: DialogManager
) -> None:
    await callback.message.delete()
    await manager.done()


button_close = Button(I18NFormat("close"), id="admin_add_close", on_click=dialog_close)
