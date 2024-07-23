import asyncio

from telethon import TelegramClient
from telethon.tl.types import (User, Chat, Channel)
from config_data.config import (Config, load_config)

config: Config = load_config(path='../.env')
api_id: str = config.tg_bot.api_id
api_hash: str = config.tg_bot.api_hash

client = TelegramClient(session='admin', api_id=api_id, api_hash=api_hash, system_version='4.16.30-vxCUSTOM"',
                        device_model='Iphone 15', app_version='10.10.10')


async def chats() -> list[dict[str, str | int]]:
    await client.start()
    chats: list[dict] = []
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, User):
            chats.append(
                {
                    'title': entity.first_name,
                    'id': entity.id
                }
            )
        elif isinstance(entity, Chat) or isinstance(entity, Channel):
            chats.append(
                {
                    'title': entity.title,
                    'id': entity.id
                }
            )
    return chats


