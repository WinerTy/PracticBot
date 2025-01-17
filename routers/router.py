from aiogram import Router

from .command import command_router


async def get_router() -> Router:
    router = Router()
    router.include_router(command_router)
    return router
