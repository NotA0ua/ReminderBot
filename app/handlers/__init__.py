from aiogram import Router

def setup_routers() -> Router:
    from . import start
    from . import language

    router = Router()

    router.include_routers(
        start.router,
        language.router,
    )

    return router
