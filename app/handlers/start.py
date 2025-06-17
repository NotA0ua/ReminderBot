from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AdminOperations
from app.utils import commands_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: types.Message, i18n: I18nContext, session: AsyncSession) -> None:
    # Check if user is admin
    admin = await AdminOperations(session).get_admin(message.from_user.id)

    await message.answer(
        i18n.get("hello", user=message.from_user.username),
        reply_markup=commands_keyboard(admin is not None),
    )
