import asyncio

from telethon import (TelegramClient, events)
from telethon.tl.types import (User, Chat, Channel)

from config_data.config import (Config, load_config)
from models.models import db
from main_loader import bot

config: Config = load_config(path='.env')
api_id: str = config.tg_bot.api_id
api_hash: str = config.tg_bot.api_hash
password: str = config.tg_bot.password

client = TelegramClient(session='admin', api_id=api_id, api_hash=api_hash, system_version='4.16.30-vxCUSTOM"',
                        device_model='Iphone 14', app_version='11.11.11')


async def get_chats() -> list[dict[str, str | int]]:
    await client.start(password=password)
    chats: list[dict] = []
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, User):
            if entity.first_name is not None:
                chats.append(
                    {
                        'title': entity.first_name,
                        'id': entity.id
                    }
                )
        elif isinstance(entity, Chat) or isinstance(entity, Channel):
            if entity.title is not None:
                chats.append(
                    {
                        'title': entity.title,
                        'id': entity.id
                    }
                )
    return chats


@client.on(events.NewMessage)
async def process_telethon_new_message_handler(event: events.NewMessage.Event):
    flags: list[tuple[int]] = (await db.select_values(name_table='users', columns='flag'))
    if (1,) in flags:
        message = event.message
        chat = await event.get_chat()
        chats = await db.select_values(name_table='chats', columns='chat_id')
        words = await db.select_values(name_table='words', columns='target_word')
        triggers = ''
        for word in words:
            if word[0] in message.text.lower().split():
                triggers += '"' + word[0] + '"' + ' '
        chati_id = (await db.select_values(name_table='users', columns='chat_id'))
        if triggers and (chat.id,) not in chati_id and (chat.id,) in chats:
            sender = await event.get_sender()
            if isinstance(sender, Channel):
                user_first_name = sender.title if sender.title else ""
                user_username = sender.username if sender.username else ""
                user_last_name = ''
            else:
                user_username = sender.username if sender.username is not None else ""
                user_first_name = sender.first_name if sender.first_name else ""
                user_last_name = sender.last_name if sender.last_name else ""

            user_channel_bot_link = f"@{user_username}" if user_username else "[НЕТ ССЫЛКИ НА ПРОФИЛЬ]"

            if hasattr(chat, 'username') and chat.username:
                message_link = f"https://t.me/{chat.username}/{message.id}"
            else:
                message_link = "[НЕТ ССЫЛКИ НА СООБЩЕНИЕ]"

            if not user_first_name and not user_last_name:
                result = (f'{message_link}\n\nТриггеры: {triggers}\n\nНайдено у(в) - {user_channel_bot_link}\n\n'
                          f'Автор: [НЕ НАЙДЕН]')

            else:
                result = (f'{message_link}\n\nТриггеры: {triggers}\n\nНайдено у(в) - {user_channel_bot_link}\n\n'
                          f'Автор: {user_first_name} {user_last_name}')
            chatic_id = await db.select_values(name_table='users', columns='chat_id', condition='flag == 1')
            bot_username = await db.select_values(name_table='users', columns='username')
            await db.update_values(name_table='users', expression='count = count + 1', condition='flag == 1')

            if message_link != "[НЕТ ССЫЛКИ НА СООБЩЕНИЕ]":
                for chat in chatic_id:
                    try:
                        await bot.send_message(chat_id=chat[0], text=result)
                    except:
                        pass
            else:
                try:
                    await client.forward_messages(entity=bot_username[0][0], from_peer=event.chat_id,
                                                  messages=[message])
                except:
                    pass


async def on_startup():
    await client.start(password=password)
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(on_startup())
