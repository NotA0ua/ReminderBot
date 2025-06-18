from aiogram import Router


def setup_admin_router() -> Router:
    from app.middlewares import AdminMiddleware
    from . import admin, admin_add

    router = Router()

    router.message.middleware(AdminMiddleware())
    router.callback_query.middleware(AdminMiddleware())

    router.include_routers(admin.router, admin_add.router)

    return router
