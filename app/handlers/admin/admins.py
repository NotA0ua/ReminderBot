from aiogram import Router, types, Bot
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import (
    Button,
    Back,
    StubScroll,
    ListGroup,
    Row,
    FirstPage,
    PrevPage,
    CurrentPage,
    NextPage,
    LastPage,
)
from aiogram_dialog.widgets.text import Format
from aiogram_i18n import LazyFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AdminOperations
from app.states import Admins
from app.utils import I18NFormat

ITEMS_PER_PAGE = 2
ID_SCROLL = "admins_scroll"

router = Router()


async def admins_handler_getter(
    bot: Bot, session: AsyncSession, dialog_manager: DialogManager, **_kwargs
) -> dict:
    admins = await AdminOperations(session).get_all_admins()

    current_page = await dialog_manager.find(ID_SCROLL).get_page()
    page_admins = (
        admins[current_page * ITEMS_PER_PAGE :]
        if len(admins) < ITEMS_PER_PAGE
        else admins[
            current_page * ITEMS_PER_PAGE : current_page * ITEMS_PER_PAGE
            + ITEMS_PER_PAGE
        ]
    )

    content = list()

    for admin in page_admins:
        user_admin = await bot.get_chat_member(admin.id, admin.id)
        content.append(
            (
                admin.id,
                (
                    user_admin.user.username
                    if user_admin.user.username
                    else user_admin.user.id
                ),
            )
        )

    return {
        "pages": (len(admins) // ITEMS_PER_PAGE) + 1,
        "current_page": current_page + 1,
        "content": content,
    }


async def admin_info_getter(bot: Bot, dialog_manager: DialogManager, **_kwargs) -> dict:
    user_id = dialog_manager.dialog_data["user_id"]
    username = (await bot.get_chat_member(user_id, user_id)).user.username
    return {
        "user_id": user_id,
        "username": f"@{username}" if username else user_id,
    }


async def admins_close(
    callback: types.CallbackQuery, _button: Button, manager: DialogManager
) -> None:
    await callback.message.delete()
    await manager.done()


async def admin_info(
    _callback: types.CallbackQuery, _button: Button, manager: DialogManager
) -> None:
    manager.dialog_data["user_id"] = int(manager.item_id)
    await manager.next()


async def admin_delete(
    _callback: types.CallbackQuery, _button: Button, manager: DialogManager
) -> None:
    user_id = manager.dialog_data["user_id"]
    session = manager.middleware_data["session"]
    await AdminOperations(session).delete_admin(user_id)
    await manager.back()


dialog = Dialog(
    Window(
        I18NFormat("admins_message"),
        ListGroup(
            Button(Format("{item[1]}"), id="admins", on_click=admin_info),
            item_id_getter=lambda i: i[0],
            items="content",
            id="admins_group",
        ),
        StubScroll(id=ID_SCROLL, pages="pages"),
        Row(
            FirstPage(
                scroll=ID_SCROLL,
                text=Format("⏮️ "),
            ),
            PrevPage(
                scroll=ID_SCROLL,
                text=Format("◀️"),
            ),
            CurrentPage(
                scroll=ID_SCROLL,
                text=Format("{current_page1}"),
            ),
            NextPage(
                scroll=ID_SCROLL,
                text=Format("▶️"),
            ),
            LastPage(
                scroll=ID_SCROLL,
                text=Format(" ⏭️"),
            ),
        ),
        Button(I18NFormat("close"), id="admins_close", on_click=admins_close),
        getter=admins_handler_getter,
        state=Admins.admins,
    ),
    Window(
        I18NFormat("admin_info"),
        Format("{username} - `{user_id}`"),
        Button(I18NFormat("delete"), id="admin_delete", on_click=admin_delete),
        Back(I18NFormat("back"), id="admin_back"),
        getter=admin_info_getter,
        state=Admins.admin,
    ),
)

router.include_router(dialog)


@router.message(LazyFilter("admins_handler"))
async def admins_handler(message_: types.Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(Admins.admins, mode=StartMode.RESET_STACK)
