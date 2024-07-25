from aiogram import (F, Router)
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import (create_words_keyboard, create_inline_keyboard)
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data == 'add', StateFilter(FSMBotStates.words))
async def process_add_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.add_word)
    await callback.message.edit_text(
        text='Введите слова для парсинга через:\nзапятую\nпробел\nперенос на новую строку',
        reply_markup=create_inline_keyboard('back', marking=1))


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.words))
async def process_back_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(text='''Привет! Я бот для парсинга сообщений. Вот что я могу:
Выбирать чаты для парсинга;
Выбирать ключевые слова для парсинга;
Парсить сообщения из всех ваших чатов. 
Используйте команды и настройки, чтобы управлять мной и настроить рассылку сообщений по вашему усмотрению!''',
                                     reply_markup=create_inline_keyboard('start_parsing', 'choose_chats',
                                                                         'choose_words', marking=(1, 2)))


@router.callback_query(F.data == 'delete', StateFilter(FSMBotStates.words))
async def process_del_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    words: list = await db.select_values(name_table='words', columns='target_word',
                                         condition=f'user_id == {callback.from_user.id}')
    await state.set_state(FSMBotStates.del_word)
    await state.set_data({'words': words})
    if len(words) > 0:
        if len(words) > 8:
            await callback.message.edit_text(text='Выбирете чат, который хотите удалить:',
                                             reply_markup=create_words_keyboard(*words[:8], flag=1))
        else:
            await callback.message.edit_text(text='Выбирете чат, который хотите удалить:',
                                             reply_markup=create_words_keyboard(*words, flag=1))
    else:
        await callback.message.edit_text(text='Нету чатов, которые вы можете удалить',
                                         reply_markup=create_inline_keyboard('back', marking=1))
