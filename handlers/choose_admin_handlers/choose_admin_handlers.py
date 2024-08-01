from aiogram import (Router, F)
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import (create_commands_keyboard, create_admin_keyboard)
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data == 'add', StateFilter(FSMBotStates.admin))
async def process_add_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.add_admin)
    await callback.message.edit_text(
        text='Введите id будущих админов бота:\n через запятую;\n через пробел;\n через перенос на новую строку.',
        reply_markup=create_commands_keyboard('back', marking=1))


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.admin))
async def process_back_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.menu)
    data = (await state.get_data())['admins']
    result = '\n'
    if data is not None:
        admins: list[tuple[int]] = [user_id for user_id in data]
        await state.update_data(admins=admins)
        if admins:
            result = '\n'.join(str(count) + ') ' + str(admin[0]) for count, admin in enumerate(admins, 1))
    await callback.message.edit_text(text=f'Текущие админы:\n{result}',
                                     reply_markup=create_commands_keyboard('delete', 'add', marking=2))


@router.callback_query(F.data == 'delete', StateFilter(FSMBotStates.admin))
async def process_del_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    admins: list[tuple[int]] | None = await db.select_values(name_table='admins', columns='user_id')
    await state.update_data(admins=admins)
    await state.set_state(FSMBotStates.del_admin)
    if admins:
        if len(admins) > 8:
            await callback.message.edit_text(text='Выбирете id админа, который хотите удалить:',
                                             reply_markup=create_admin_keyboard(*admins[:8], flag=1))
        else:
            await callback.message.edit_text(text='Выбирете id админа, который хотите удалить:',
                                             reply_markup=create_admin_keyboard(*admins, flag=1))
    else:
        await callback.message.edit_text(text='Нету id админов, которые вы можете удалить',
                                         reply_markup=create_commands_keyboard('back', marking=1))
