from aiogram_dialog import Dialog

from . import admins, admin_add


def dialogs() -> list[Dialog]:
    return [admins.dialog, admin_add.dialog]
