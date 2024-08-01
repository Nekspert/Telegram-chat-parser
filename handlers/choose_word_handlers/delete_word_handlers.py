from aiogram import (Router, F)
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import (create_words_keyboard, create_commands_keyboard)
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data.startswith('forward'), StateFilter(FSMBotStates.del_word))
async def process_forward_del_command(callback: CallbackQuery, state: FSMContext) -> None:
    chatics = (await state.get_data())['words']
    index = int(callback.data.split('_')[1])
    if 0 < len(chatics[index * 8: (index + 1) * 8]) <= 8:
        await callback.message.edit_reply_markup(
            reply_markup=create_words_keyboard(*chatics[index * 8: (index + 1) * 8], flag=index + 1))
    await callback.answer()


@router.callback_query(F.data.startswith('backward'), StateFilter(FSMBotStates.del_word))
async def process_backward_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    if int(callback.data.split('_')[1]) > 1:
        chatics = (await state.get_data())['words']
        index: int = int(callback.data.split('_')[1])
        await callback.message.edit_reply_markup(
            reply_markup=create_words_keyboard(*chatics[(index - 2) * 8: (index - 1) * 8], flag=index - 1))
    await callback.answer()


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.del_word))
async def process_back_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    words: list = await db.select_values(name_table='words', columns='target_word',
                                         condition=f'user_id == {callback.from_user.id}')
    await state.set_state(FSMBotStates.words)
    if len(words) == 0:
        await callback.message.edit_text(text='Слова для парсинга не выбраны',
                                         reply_markup=create_commands_keyboard('delete', 'add', 'back', marking=2))
    else:
        target_words = '\n'.join(f'{i}) {word[0][:30]}' for i, word in enumerate(words, 1))
        await callback.message.edit_text(text='Ключевые слова для парсинга:\n' + target_words,
                                         reply_markup=create_commands_keyboard(
                                             'delete', 'add', 'back', marking=2
                                         ))


@router.callback_query(StateFilter(FSMBotStates.del_word))
async def process_del_word_command(callback: CallbackQuery) -> None:
    await db.delete_row(name_table='words',
                        condition=f'user_id == {callback.from_user.id} AND target_word == "{callback.data}"')
    await callback.answer(text=f'{callback.data} - удален(а)')
