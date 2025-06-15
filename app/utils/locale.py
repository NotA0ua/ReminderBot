from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton
from aiogram_i18n.utils.language_inline_keyboard import LanguageInlineMarkup

lang_kb = LanguageInlineMarkup(
    key="lang_button",
    hide_current=True,
    param="locale",
    keyboard=[[InlineKeyboardButton(text=LazyProxy("back"), callback_data="back_lang")]],
)
