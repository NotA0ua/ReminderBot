import logging
from asyncio import sleep

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.locale import locale_kb

router = Router(name=__name__)

@router.message(Command("lang"))
async def lang_handler(message: types.Message, i18n: I18nContext) -> None:
    await locale_kb.startup(i18n)

    logging.info(locale_kb)
    await message.reply(
        i18n.get("lang", i18n.locale), reply_markup=locale_kb.reply_markup()
    )

@router.callback_query(locale_kb.filter)
async def change_locale_handler(callback: types.CallbackQuery, locale: str, i18n: I18nContext, session: AsyncSession) -> None:
    await i18n.set_locale(locale=locale)
    result_message = await callback.message.answer(i18n.get("lang_result", i18n.locale))
    await callback.message.delete()
    await session.commit()
    await sleep(5)
    await result_message.delete()

@router.callback_query(F.data == "back_lang")
async def lang_handler(callback: types.CallbackQuery, i18n: I18nContext) -> None:
    await callback.message.delete()