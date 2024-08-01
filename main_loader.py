from aiogram import (Bot, Dispatcher)

from config_data.config import (Config, load_config)
from models.models import db

config: Config = load_config('.env')
admins: list[int] = config.tg_bot.admin_ids

bot = Bot(token=config.tg_bot.token)

dp = Dispatcher()
dp.workflow_data.update(
    {'instance_bot': bot, 'admin_ids': admins, 'super_admin': admins[0]}
)


async def db_loader():
    await db.create_table(name_table='users',
                          columns=(
                              ('user_id', 'INTEGER'), ('user_name', 'TEXT'), ('flag', 'INTEGER'), ('count', 'INTEGER'),
                              ('chat_id', 'INTEGER'), ('username', 'TEXT')))
    await db.create_table(name_table='admins', columns=(('user_id', 'INTEGER'),))
    await db.create_table(name_table='chats',
                          columns=(('user_id', 'INTEGER'), ('chat_title', 'TEXT'), ('chat_id', 'INTEGER')))
    await db.create_table(name_table='words', columns=(('user_id', 'INTEGER'), ('target_word', 'TEXT')))
