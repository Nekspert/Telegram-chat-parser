from aiogram import (Router, F)
from aiogram.filters import (Command, StateFilter)
from aiogram.types import (Message, CallbackQuery)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from filters.admin_filter import IsAdmin
from models.models import db
from keyboards.keyboard_utils import create_inline_keyboard
from states.bot_states import FSMBotStates

router = Router()


@router.message(Command(commands=['start']), IsAdmin(), StateFilter(default_state))
async def process_start_command(message: Message) -> None:
    await db.create_table(name_table='users', columns=(('user_id', 'INTEGER'), ('user_name', 'TEXT')))
    await db.create_table(name_table='chats',
                          columns=(('user_id', 'INTEGER'), ('chat_title', 'TEXT'), ('chat_id', 'INTEGER')))
    await db.create_table(name_table='words', columns=(('user_id', 'INTEGER'), ('target_word', 'TEXT')))

    await db.add_values_unique(name_table='users', values=(message.from_user.id, f'@{message.from_user.username}'))

    await message.answer(text='''Привет! Я бот для парсинга сообщений. Вот что я могу:
Выбирать чаты для парсинга;
Выбирать ключевые слова для парсинга;
Парсить сообщения из всех ваших чатов. 
Используйте команды и настройки, чтобы управлять мной и настроить рассылку сообщений по вашему усмотрению!''',
                         reply_markup=create_inline_keyboard('start_parsing', 'choose_chats', 'choose_words',
                                                             marking=(1, 2)))


@router.message(Command(commands=['cancel']), IsAdmin(), StateFilter(default_state))
async def process_none_cancel_command(message: Message) -> None:
    await message.answer(text='Вы вне взаимодействия с ботом!\nДля взаимодействия введите команду /start')


@router.message(Command(commands=['cancel']), IsAdmin(), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text='Вы вышли из взаимодействия с ботом.\nДля взаимодействия введите команду /start')


@router.callback_query(F.data == 'choose_chats')
async def process_choose_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    chats = await db.select_values(name_table='chats', columns=('chat_title', 'chat_id'),
                                   condition=f'user_id == {callback.from_user.id}')
    await state.set_state(FSMBotStates.chats)
    await state.set_data({'chats_in_lists_del': chats})
    # print(chats)
    if len(chats) == 0:
        await callback.message.edit_text(text='Чаты для парсинга не выбраны',
                                         reply_markup=create_inline_keyboard('delete', 'add', 'back', marking=2))
    else:
        target_chats = '\n'.join(f'{i}) {chat[0][:50]}' for i, chat in enumerate(chats, 1))
        await callback.message.edit_text(text='Чаты для парсинга:\n' + target_chats,
                                         reply_markup=create_inline_keyboard(
                                             'delete', 'add', 'back', marking=2
                                         ))


@router.callback_query(F.data == 'choose_words')
async def process_target_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    words = await db.select_values(name_table='words', columns='target_word',
                                   condition=f'user_id == {callback.from_user.id}')
    await state.set_state(FSMBotStates.words)
    if len(words) == 0:
        await callback.message.edit_text(text='Слова для парсинга не выбраны',
                                         reply_markup=create_inline_keyboard('delete', 'add', 'back', marking=2))
    else:
        target_words = '\n'.join(f'{i}) {word[0][:30]}' for i, word in enumerate(words, 1))
        await callback.message.edit_text(text='Ключевые слова для парсинга:\n' + target_words,
                                         reply_markup=create_inline_keyboard(
                                             'delete', 'add', 'back', marking=2
                                         ))


# template
@router.callback_query(F.data == 'start_parsing')
async def process_start_parsing_command(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text='Парсинг запущен')


@router.message(IsAdmin(), StateFilter(default_state))
async def process_echo_admin2_command(message: Message) -> None:
    await message.answer(text='Я вас не понимаю! Действуйте по инструкциям бота.')


@router.message(StateFilter(default_state))
async def process_echo_command(message: Message) -> None:
    await message.answer(text='У вас нет права пользоваться данным ботом.')
