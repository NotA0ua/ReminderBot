from aiogram import Router

from app.middlewares import AdminMiddleware


def setup_admin_router() -> Router:
    from . import admin

    router = Router()

    router.message.middleware(AdminMiddleware())
    router.callback_query.middleware(AdminMiddleware())

    router.include_routers(
        admin.router
    )

    return router
