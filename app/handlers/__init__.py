from aiogram import Router

def setup_routers() -> Router:
    from . import start
    from . import locale

    router = Router()

    router.include_routers(
        start.router,
        locale.router,
    )

    return router
