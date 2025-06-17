from aiogram_i18n import LazyProxy, types
from aiogram_i18n.utils.language_inline_keyboard import LanguageInlineMarkup


def locale_keyboard() -> LanguageInlineMarkup:
    from aiogram_i18n.types import InlineKeyboardButton

    return LanguageInlineMarkup(
        key="locale_button",
        hide_current=True,
        param="locale",
        keyboard=[
            [InlineKeyboardButton(text=LazyProxy("back"), callback_data="back_locale")]
        ],
    )


def commands_keyboard(is_admin: bool = False) -> types.ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text=LazyProxy("locale_handler"))]]
    if is_admin:
        admin_kb = [types.KeyboardButton(text=LazyProxy("admin_handler"))]
        kb.append(admin_kb)

    return types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, is_persistent=True
    )


def admin_commands_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text=LazyProxy("admin_exit_handler"))]]

    return types.ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, is_persistent=True
    )
