from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_i18n import I18nContext

router = Router(name=__name__)


@router.message(CommandStart)
async def start_handler(message: types.Message, i18n: I18nContext) -> None:
    await message.answer(
        i18n.get("hello", user=message.from_user.username),
    )
