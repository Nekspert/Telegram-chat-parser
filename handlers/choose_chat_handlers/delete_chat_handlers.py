from aiogram import (Router, F)
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import (create_chats_keyboard, create_commands_keyboard)
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data.startswith('forward'), StateFilter(FSMBotStates.del_chat))
async def process_forward_del_command(callback: CallbackQuery, state: FSMContext) -> None:
    chatics = (await state.get_data())['chats_in_lists_del']
    index = int(callback.data.split('_')[1])
    if 0 < len(chatics[index * 8: (index + 1) * 8]) <= 8:
        await callback.message.edit_reply_markup(
            reply_markup=create_chats_keyboard(*chatics[index * 8: (index + 1) * 8], flag=index + 1))
    await callback.answer()


@router.callback_query(F.data.startswith('backward'), StateFilter(FSMBotStates.del_chat))
async def process_backward_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    if int(callback.data.split('_')[1]) > 1:
        chatics = (await state.get_data())['chats_in_lists_del']
        index: int = int(callback.data.split('_')[1])
        await callback.message.edit_reply_markup(
            reply_markup=create_chats_keyboard(*chatics[(index - 2) * 8: (index - 1) * 8], flag=index - 1))
    await callback.answer()


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.del_chat))
async def process_back_add_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.chats)
    chats = await db.select_values(name_table='chats', columns=('chat_title', 'chat_id'),
                                   condition=f'user_id == {callback.from_user.id}')
    await state.update_data(chats_in_lists_del=chats)
    if len(chats) == 0:
        await callback.message.edit_text(text='Чаты для парсинга не выбраны',
                                         reply_markup=create_commands_keyboard('delete', 'add', 'back', marking=2))
    else:
        target_chats = '\n'.join(f'{i}) {chat[0][:50]}' for i, chat in enumerate(chats, 1))
        await callback.message.edit_text(text='Чаты для парсинга:\n' + target_chats,
                                         reply_markup=create_commands_keyboard(
                                             'delete', 'add', 'back', marking=2
                                         ))


@router.callback_query(StateFilter(FSMBotStates.del_chat))
async def process_delete_command(callback: CallbackQuery, state: FSMContext) -> None:
    title = [name for name in (await state.get_data())['chats_in_lists_del'] if name['id'] == int(callback.data)]
    await db.delete_row(name_table='chats',
                        condition=f'user_id == {callback.from_user.id} AND chat_id == {callback.data}')
    await callback.answer(text=f'{title} - удален(а)')
