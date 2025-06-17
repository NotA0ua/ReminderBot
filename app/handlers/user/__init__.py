from aiogram import Router


def setup_user_router() -> Router:
    from . import locale, start

    router = Router()

    router.include_routers(
        start.router,
        locale.router,
    )

    return router
