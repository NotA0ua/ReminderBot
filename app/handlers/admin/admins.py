import logging

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

from app.database import AdminOperations, Admin
from app.utils import I18NFormat
from app.states import Admins

ITEMS_PER_PAGE = 2
ID_SCROLL = "admins_scroll"

router = Router()


async def admins_handler_getter(
    bot: Bot, session: AsyncSession, dialog_manager: DialogManager, **_kwargs
) -> dict:
    # session: AsyncSession = dialog_manager.middleware_data[""]

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
        content.append([admin.id, user_admin.user.username if user_admin.user.username else user_admin.user.id])

    logging.info(content)

    return {
        "pages": (len(admins) // ITEMS_PER_PAGE) + 1,
        "current_page": current_page + 1,
        "content": content,
    }


async def admin_info() -> None: ...


dialog = Dialog(
    Window(
        I18NFormat("admins_message"),
        ListGroup(
            Button(Format("{item[1]}"), id="admins", on_click=...),
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
        Button(I18NFormat("close"), id="admins_close", on_click=...),
        getter=admins_handler_getter,
        state=Admins.admins,
    ),
    Window(
        I18NFormat("admin_info"),
        Button(I18NFormat("delete"), id="admin_delete", on_click=...),
        Back(I18NFormat("back"), id="admin_back"),
        state=Admins.admin,
    ),
)

router.include_router(dialog)


@router.message(LazyFilter("admins_handler"))
async def admins_handler(_message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Admins.admins, mode=StartMode.RESET_STACK)
