import asyncio

from handlers import (menu_handlers, choose_chat_handlers, choose_word_handlers, choose_admin_handlers)
from keyboards.menu_keyboard import set_menu
from services.user_bot import on_startup
from main_loader import (bot, dp, db_loader)


async def main() -> None:
    await db_loader()
    dp.include_router(menu_handlers.router)

    dp.include_router(choose_admin_handlers.add_admin_handlers.router)
    dp.include_router(choose_admin_handlers.choose_admin_handlers.router)
    dp.include_router(choose_admin_handlers.delete_admin_handlers.router)

    dp.include_router(choose_chat_handlers.add_chat_handlers.router)
    dp.include_router(choose_chat_handlers.choose_chat_handlers.router)
    dp.include_router(choose_chat_handlers.delete_chat_handlers.router)

    dp.include_router(choose_word_handlers.add_word_handlers.router)
    dp.include_router(choose_word_handlers.choose_word_handlers.router)
    dp.include_router(choose_word_handlers.delete_word_handlers.router)

    await set_menu(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(on_startup(), dp.start_polling(bot))


if __name__ == '__main__':
    asyncio.run(main())
