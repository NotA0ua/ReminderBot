from aiogram import Router, types
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import LazyFilter
from aiogram_dialog import Dialog, Window, DialogManager, StartMode

from app.utils import AdminAdd, I18NFormat

router = Router()


dialog = Dialog(
    Window(I18NFormat("admin_add_handler"), Button(I18NFormat("back"), id="admin_add_back"), state=AdminAdd.admin_add),
)

router.include_router(dialog)

@router.message(LazyFilter("admin_add_handler"))
async def admin_add_handler(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminAdd.admin_add, mode=StartMode.RESET_STACK)
