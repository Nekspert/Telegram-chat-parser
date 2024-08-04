from aiogram import (Router, F)
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import (create_admin_keyboard, create_commands_keyboard)
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data.startswith('forward'), StateFilter(FSMBotStates.del_admin))
async def process_forward_del_command(callback: CallbackQuery, state: FSMContext) -> None:
    admins = (await state.get_data())['admins']
    index = int(callback.data.split('_')[1])
    if 0 < len(admins[index * 8: (index + 1) * 8]) <= 8:
        await callback.message.edit_reply_markup(
            reply_markup=create_admin_keyboard(*admins[index * 8: (index + 1) * 8], flag=index + 1))
    await callback.answer()


@router.callback_query(F.data.startswith('backward'), StateFilter(FSMBotStates.del_admin))
async def process_backward_chat_command(callback: CallbackQuery, state: FSMContext) -> None:
    if int(callback.data.split('_')[1]) > 1:
        admins = (await state.get_data())['admins']
        index: int = int(callback.data.split('_')[1])
        await callback.message.edit_reply_markup(
            reply_markup=create_admin_keyboard(*admins[(index - 2) * 8: (index - 1) * 8], flag=index - 1))
    await callback.answer()


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.del_admin))
async def process_back_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.admin)
    data: list[tuple[int]] | None = await db.select_values(name_table='admins', columns='user_id')

    result = '\n'
    if data is not None:
        admins: list[tuple[int]] = [user_id for user_id in data]
        await state.update_data(admins=admins)
        if admins:
            result = '\n'.join(str(count) + ') ' + str(admin[0]) for count, admin in enumerate(admins, 1))
    await callback.message.edit_text(text=f'Текущие админы:\n{result}',
                                     reply_markup=create_commands_keyboard('delete', 'add', marking=2))


@router.callback_query(StateFilter(FSMBotStates.del_admin))
async def process_del_word_command(callback: CallbackQuery) -> None:
    await db.delete_row(name_table='admins',
                        condition=f'user_id == {callback.data}')
    await db.delete_row(name_table='users',
                        condition=f'user_id == {callback.data}')
    await callback.answer(text=f'ID: {callback.data} - удален')
