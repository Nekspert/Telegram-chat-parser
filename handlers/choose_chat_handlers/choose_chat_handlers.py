from aiogram import (Router, F)
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.keyboard_utils import (create_chats_keyboard, create_inline_keyboard)
from states.bot_states import FSMBotStates
from services.user_bot import get_chats

router = Router()


@router.callback_query(F.data == 'add', StateFilter(FSMBotStates.chats))
async def process_add_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.add_chat)
    chatics = await get_chats()
    # print(chatics[:2])
    await state.set_data({'chats_in_list': chatics})
    if len(chatics) > 8:
        await callback.message.edit_text(text='Выбирете чат, который хотите парсить:',
                                         reply_markup=create_chats_keyboard(*chatics[:8], flag=1))
    else:
        await callback.message.edit_text(text='Выбирете чат, который хотите парсить:',
                                         reply_markup=create_chats_keyboard(*chatics, flag=1))


@router.callback_query(F.data == 'delete', StateFilter(FSMBotStates.chats))
async def process_delete_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    chatics = (await state.get_data())['chats_in_lists_del']
    await state.set_state(FSMBotStates.del_chat)

    print('process_delete_chat_command', chatics)
    if len(chatics) > 0:
        chats: list[dict] = []
        for title, chat_id in chatics:
            chats.append({'title': title, 'id': chat_id})
        await state.set_data({'chats_in_lists_del': chats})
        if len(chats) > 8:
            await callback.message.edit_text(text='Выбирете чат, который хотите удалить:',
                                             reply_markup=create_chats_keyboard(*chats[:8], flag=1))
        else:
            await callback.message.edit_text(text='Выбирете чат, который хотите удалить:',
                                             reply_markup=create_chats_keyboard(*chats, flag=1))
    else:
        await callback.message.edit_text(text='Нету чатов, которые вы можете удалить',
                                         reply_markup=create_inline_keyboard('back', marking=1))


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.chats))
async def process_back_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(text='''Привет! Я бот для парсинга сообщений. Вот что я могу:
Выбирать чаты для парсинга;
Выбирать ключевые слова для парсинга;
Парсить сообщения из всех ваших чатов. 
Используйте команды и настройки, чтобы управлять мной и настроить рассылку сообщений по вашему усмотрению!''',
                                     reply_markup=create_inline_keyboard('start_parsing', 'choose_chats',
                                                                         'choose_words', marking=(1, 2)))
