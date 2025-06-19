from aiogram import Router


def setup_admin_router() -> Router:
    from app.middlewares import AdminMiddleware
    from . import admin, admins

    router = Router()

    router.message.middleware(AdminMiddleware())
    router.callback_query.middleware(AdminMiddleware())

    router.include_routers(admin.router, admins.router)

    return router
