import logging
from asyncio import sleep

from aiogram import Router, types, F
from aiogram_i18n import I18nContext, LazyFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import locale_keyboard
from .start import start_handler

router = Router(name=__name__)


locale_kb = locale_keyboard()


@router.message(LazyFilter("locale_handler"))
async def lang_handler(message: types.Message, i18n: I18nContext) -> None:
    await locale_kb.startup(i18n)

    logging.info(locale_kb)
    await message.reply(
        i18n.get("locale", i18n.locale), reply_markup=locale_kb.reply_markup()
    )


@router.callback_query(locale_kb.filter)
async def change_locale_handler(
    callback: types.CallbackQuery, locale: str, i18n: I18nContext, session: AsyncSession
) -> None:
    await i18n.set_locale(locale=locale)
    await callback.message.delete()
    await session.commit()
    await start_handler(callback.message, i18n, session, callback.from_user.id)


@router.callback_query(F.data == "back_locale")
async def lang_handler(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
