from aiogram import (Router, F)
from aiogram.types import (CallbackQuery, Message)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import create_inline_keyboard
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.add_word))
async def process_back_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.words)
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


@router.callback_query(F.data == 'yes', StateFilter(FSMBotStates.add_word))
async def process_add_yes_command(callback: CallbackQuery, state: FSMContext) -> None:
    result_words: list[str] = (await state.get_data())['words']
    for word in result_words:
        await db.add_values_repetitive(name_table='words', values=(callback.from_user.id, word))
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


@router.callback_query(F.data == 'no', StateFilter(FSMBotStates.add_word))
async def process_add_yes_command(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Введите слова для парсинга через:\nзапятую\nпробел\nперенос на новую строку',
        reply_markup=create_inline_keyboard('back', marking=1))


@router.message(StateFilter(FSMBotStates.add_word))
async def process_get_word_command(message: Message, state: FSMContext) -> None:
    result_words: list[str] = message.text.replace('\n', ' ').replace(',',
                                                                      ' ').replace('"', "'").split()
    await state.set_data({'words': result_words})
    text = '\n'.join(str(count) + ') ' + word.strip() for count, word in enumerate(result_words, 1))
    await message.answer(text=text,
                         reply_markup=create_inline_keyboard('no', 'yes', 'back', marking=(2, 1)))
