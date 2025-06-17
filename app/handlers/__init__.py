from aiogram import Router


def setup_routers() -> Router:
    from .user import setup_user_router
    from .admin import setup_admin_router

    router = Router()

    router.include_routers(
        setup_user_router(),
        setup_admin_router(),
    )

    return router
