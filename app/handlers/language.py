import logging

from aiogram import Router, types
from aiogram.filters import Command
from aiogram_i18n import I18nContext, LazyProxy
from aiogram_i18n.types import InlineKeyboardButton
from aiogram_i18n.utils.language_inline_keyboard import LanguageInlineMarkup

router = Router(name=__name__)

lang_kb = LanguageInlineMarkup(
        key="lang",
        # hide_current=False,
        keyboard=[[InlineKeyboardButton(text=LazyProxy("back"), callback_data="back")]],
    )


@router.message(Command("lang"))
async def lang(message: types.Message, i18n: I18nContext):
    logging.info(lang_kb.keyboards)
    await message.reply(
        i18n.get("lang", i18n.locale), reply_markup=lang_kb.reply_markup()
    )
