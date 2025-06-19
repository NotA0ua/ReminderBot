from aiogram import Router, types
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Keyboard
from aiogram_dialog.widgets.text import Const
from aiogram_i18n import LazyFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AdminOperations
from app.utils import I18NFormat
from app.states import Admins

router = Router()

async def admins_buttons(callback_or_message: types.CallbackQuery | types.Message, session: AsyncSession) -> list[Button]:
    buttons = list()
    admins = await AdminOperations(session).get_all_admins()
    for admin in admins:
        user_admin = await callback_or_message.bot.get_chat_member(admin.id, admin.id)
        buttons.append(Button(Const(user_admin.user.username), id=f"admin_{admin.id}"))

    return buttons

async def admins_handler_getter(callback_or_message: types.CallbackQuery | types.Message, session: AsyncSession):
    return {
        "buttons": await admins_buttons(callback_or_message, session),
    }


dialog = Dialog(
    Window(
        I18NFormat("admins_handler_message"),
        StubScroll(id=ID_STUB_SCROLL, pages="pages"),
        NumberedPager(scroll=ID_STUB_SCROLL),
        Button(I18NFormat("close"), id="admins_close"),
        state=Admins.admin_add,
        getter=admins_handler_getter,
    ),
    # Window(
    #     state=Admins.admin_id,
    #     getter=paging_getter,
    #     preview_data=paging_getter,
    # )
)

router.include_router(dialog)

@router.message(LazyFilter("admins_handler"))
async def admins_handler(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminAdd.admin_add, mode=StartMode.RESET_STACK)
