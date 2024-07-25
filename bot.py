import asyncio
from aiogram import (Bot, Dispatcher)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import (Config, load_config)
from handlers import (menu_handlers, choose_chat_handlers, choose_word_handlers)
from keyboards.menu_keyboard import set_menu


async def main() -> None:
    config: Config = load_config(path='.env')
    bot = Bot(
        token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.workflow_data.update(
        {
            'instance_bot': bot, 'admin_ids': config.tg_bot.admin_ids
        }
    )

    dp.include_router(menu_handlers.router)
    dp.include_router(choose_chat_handlers.add_chat_handlers.router)
    dp.include_router(choose_chat_handlers.choose_chat_handlers.router)
    dp.include_router(choose_chat_handlers.delete_chat_handlers.router)
    dp.include_router(choose_word_handlers.add_word_handlers.router)
    dp.include_router(choose_word_handlers.choose_word_handlers.router)
    dp.include_router(choose_word_handlers.delete_word_handlers.router)

    await set_menu(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
