from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart)
async def start_handler(message: types.Message) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}!\nThis is a reminder bot. It allows you to easily create scheduled reminders."
    )
