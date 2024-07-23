from aiogram.types import BotCommand
from aiogram import Bot


async def set_menu(bot: Bot) -> None:
    main_menu_commands: list[BotCommand] = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/cancel', description='Выход из диалога с ботом')
    ]
    await bot.set_my_commands(commands=main_menu_commands)
