from aiogram import (Router, F)
from aiogram.filters import (Command, StateFilter)
from aiogram.types import (Message, CallbackQuery)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from filters.admin_filter import (IsAdmin, SuperAdmin)
from models.models import db
from keyboards.keyboard_utils import create_commands_keyboard
from states.bot_states import FSMBotStates

router = Router()


@router.message(Command(commands=['start']), IsAdmin(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext, instance_bot) -> None:
    await state.set_state(FSMBotStates.menu)
    username = await instance_bot.get_me()

    await db.add_values_unique(name_table='users',
                               values=(message.from_user.id, f'@{message.from_user.username}', 0, 0, message.chat.id,
                                       f'@{username.username}'))

    await message.answer(text='''Привет! Я бот для парсинга сообщений. Вот что я могу:
    Выбирать чаты для парсинга;
    Выбирать ключевые слова для парсинга;
    Парсить сообщения из всех ваших чатов. 
Используйте команды и настройки, чтобы управлять мной и настроить парсинг сообщений по вашему усмотрению!''',
                         reply_markup=create_commands_keyboard('start_parsing', 'choose_chats_start',
                                                               'choose_words_start', marking=(1, 2)))


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.menu))
async def process_start_back_command(callback: CallbackQuery) -> None:
    await callback.message.edit_text(text='''Привет! Я бот для парсинга сообщений. Вот что я могу:
    Выбирать чаты для парсинга;
    Выбирать ключевые слова для парсинга;
    Парсить сообщения из всех ваших чатов. 
Используйте команды и настройки, чтобы управлять мной и настроить рассылку сообщений по вашему усмотрению!''',
                                     reply_markup=create_commands_keyboard('start_parsing', 'choose_chats_start',
                                                                           'choose_words_start', marking=(1, 2)))


@router.message(Command(commands=['cancel']), IsAdmin(), StateFilter(default_state))
async def process_none_cancel_command(message: Message) -> None:
    await message.answer(text='Вы вне взаимодействия с ботом!\nДля взаимодействия введите команду /start')


@router.message(Command(commands=['cancel']), IsAdmin(), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await db.update_values(name_table='users', expression='(flag = 0) AND (count = 0)',
                           condition=f'user_id == {message.from_user.id}')
    await message.answer(text='Вы вышли из взаимодействия с ботом.\nДля взаимодействия введите команду /start')


@router.message(Command(commands=['admins']), SuperAdmin())
async def process_admin_command(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.admin)
    admins: list[tuple[int]] | None = await db.select_values(name_table='admins', columns='user_id')
    await state.update_data(admins=admins)
    if admins:
        result = '\n'.join(str(count) + ') ' + str(admin[0]) for count, admin in enumerate(admins, 1))
    else:
        result = '\n'
    await message.answer(text=f'Текущие админы:\n{result}',
                         reply_markup=create_commands_keyboard('delete', 'add', marking=2))


@router.message(Command(commands=['admins']), IsAdmin())
async def process_admin_command(message: Message) -> None:
    await message.answer(text=f'Вы не имеете права добавлять админов')


@router.message(Command(commands=['menu']), IsAdmin())
async def process_menu_command(message: Message, state: FSMContext) -> None:
    flag, count = (await db.select_values(name_table='users', columns=('flag', 'count'),
                                          condition=f'user_id == {message.from_user.id}'))[0]
    await state.clear()
    await state.set_state(FSMBotStates.menu)
    if flag:
        await message.answer(
            text=f'Бот в состоянии парсинга. Спарсено - {count} сообщений(я)\n\n'
                 f'Бот в реальном времени проверяет чаты и ключевые слова. '
                 f'Перезапускать его после изменения настроек - не нужно.'
                 f'\n\nОтсюда во время парсинга вы можете изменять настройки.',
            reply_markup=create_commands_keyboard('end_parsing', 'choose_chats_menu',
                                                  'choose_words_menu', marking=(1, 2)))
    else:
        await message.answer(
            text=f'Бот в выключенном состоянии.\n'
                 f'Бот в реальном времени проверяет чаты и ключевые слова.'
                 f'\nПерезапускать его после изменения настроек - не нужно.'
                 f'\n\nОтсюда во время парсинга вы можете изменять настройки.',
            reply_markup=create_commands_keyboard('start_parsing', 'choose_chats_menu',
                                                  'choose_words_menu', marking=(1, 2)))


@router.callback_query(F.data.startswith('choose_chats'), StateFilter(FSMBotStates.menu))
async def process_choose_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    chats = await db.select_values(name_table='chats', columns=('chat_title', 'chat_id'))
    try:
        choice = (await state.get_data())['choice']
        if choice == 'start' and callback.data.split('_')[-1] == 'menu':
            await state.set_state(FSMBotStates.chats)
            await state.update_data(choice='menu')
        elif choice == 'menu' and callback.data.split('_')[-1] == 'start':
            await state.set_state(FSMBotStates.chats)
            await state.update_data(choice='start')
        else:
            await state.set_state(FSMBotStates.chats)
            await state.update_data(choice=choice)
    except:
        await state.set_state(FSMBotStates.chats)
        await state.update_data(choice=callback.data.split('_')[-1])

    await state.update_data(chats_in_lists_del=chats)

    if len(chats) == 0:
        await callback.message.edit_text(text='Чаты для парсинга не выбраны',
                                         reply_markup=create_commands_keyboard('delete', 'add',
                                                                               'back', marking=2))
    else:
        target_chats = '\n'.join(f'{i}) {chat[0][:50]}' for i, chat in enumerate(chats, 1))
        await callback.message.edit_text(text='Чаты для парсинга:\n' + target_chats,
                                         reply_markup=create_commands_keyboard(
                                             'delete', 'add', 'back', marking=2
                                         ))


@router.callback_query(F.data.startswith('choose_words'), StateFilter(FSMBotStates.menu))
async def process_target_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    words = await db.select_values(name_table='words', columns='target_word')
    try:
        choice = (await state.get_data())['choice']
        if choice == 'start' and callback.data.split('_')[-1] == 'menu':
            await state.set_state(FSMBotStates.words)
            await state.update_data(choice='menu')
        elif choice == 'menu' and callback.data.split('_')[-1] == 'start':
            await state.set_state(FSMBotStates.words)
            await state.update_data(choice='start')
        else:
            await state.set_state(FSMBotStates.words)
            await state.update_data(choice=choice)
    except:
        await state.set_state(FSMBotStates.words)
        await state.update_data(choice=callback.data.split('_')[-1])

    if len(words) == 0:
        await callback.message.edit_text(text='Слова для парсинга не выбраны',
                                         reply_markup=create_commands_keyboard('delete', 'add',
                                                                               'back',
                                                                               marking=2))
    else:
        target_words = '\n'.join(f'{i}) {word[0][:30]}' for i, word in enumerate(words, 1))
        await callback.message.edit_text(text='Ключевые слова для парсинга:\n' + target_words,
                                         reply_markup=create_commands_keyboard(
                                             'delete', 'add', 'back', marking=2
                                         ))


# template
@router.callback_query(F.data == 'start_parsing', StateFilter(FSMBotStates.menu))
async def process_start_parsing_command(callback: CallbackQuery) -> None:
    await db.update_values(name_table='users', expression='flag = 1', condition=f'user_id == {callback.from_user.id}')
    chats = (await db.select_values(name_table='chats', columns='chat_id'))
    words = (await db.select_values(name_table='words', columns='target_word'))
    if len(words) == 0 or len(chats) == 0:
        await callback.message.edit_text(
            text='Вы не ввели нужные данные для парсинга!\nВведите данные и повторите попытку.',
            reply_markup=create_commands_keyboard('back', marking=1))
    else:
        count = (await db.select_values(name_table='users', columns='count',
                                        condition=f'user_id == {callback.from_user.id}'))[0][0]
        await callback.message.edit_text(
            text=f'Бот в состоянии парсинга. Спарсено - {count} сообщений(я)\n\n'
                 f'Бот в реальном времени проверяет чаты и ключевые слова. '
                 f'Перезапускать его после изменения настроек - не нужно.'
                 f'\n\nОтсюда во время парсинга вы можете изменять настройки.',
            reply_markup=create_commands_keyboard('end_parsing', 'choose_chats_menu', 'choose_words_menu',
                                                  marking=(1, 2)))


@router.callback_query(F.data == 'end_parsing', StateFilter(FSMBotStates.menu))
async def process_end_parsing_command(callback: CallbackQuery) -> None:
    await db.update_values(name_table='users', expression='flag = 0', condition=f'user_id == {callback.from_user.id}')
    await db.update_values(name_table='users', expression='count = 0', condition=f'user_id == {callback.from_user.id}')
    await callback.message.edit_text(text=f'Бот в выключенном состоянии.\n'
                                          f'Бот в реальном времени проверяет чаты и ключевые слова.'
                                          f'\nПерезапускать его после изменения настроек - не нужно.'
                                          f'\n\nОтсюда во время парсинга вы можете изменять настройки.',
                                     reply_markup=create_commands_keyboard('start_parsing', 'choose_chats_menu',
                                                                           'choose_words_menu',
                                                                           marking=(1, 2)))


@router.message(IsAdmin(), StateFilter(default_state))
async def process_echo_admin2_command(message: Message) -> None:
    await message.answer(text='Я вас не понимаю! Действуйте по инструкциям бота.')


@router.message(StateFilter(default_state))
async def process_echo_command(message: Message) -> None:
    await message.answer(text='У вас нет права пользоваться данным ботом.')
