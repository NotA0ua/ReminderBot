from aiogram import Router, types
from aiogram.filters import Command
from aiogram_i18n import I18nContext

from app.utils.language import language_keyboard

router = Router(name=__name__)


@router.message(Command("lang"))
async def lang(message: types.Message, i18n: I18nContext):
    await message.reply(
        i18n.get("cur-lang", i18n.locale), reply_markup=language_keyboard()
    )
