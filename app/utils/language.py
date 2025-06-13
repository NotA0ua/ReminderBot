from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton
from aiogram_i18n.utils.language_inline_keyboard import LanguageInlineMarkup


def language_keyboard() -> LanguageInlineMarkup:
    return LanguageInlineMarkup(
        key="lang",
        hide_current=False,
        keyboard=[[InlineKeyboardButton(text=LazyProxy("back"), callback_data="back")]],
    )
