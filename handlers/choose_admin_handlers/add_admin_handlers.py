from aiogram import (Router, F)
from aiogram.types import (CallbackQuery, Message)
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from models.models import db
from keyboards.keyboard_utils import create_commands_keyboard
from states.bot_states import FSMBotStates

router = Router()


@router.callback_query(F.data == 'back', StateFilter(FSMBotStates.add_admin))
async def process_back_word_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FSMBotStates.admin)
    data = (await state.get_data())['admins']
    result = '\n'
    if data is not None:
        admins: list[tuple[int]] = [user_id for user_id in data]
        if admins:
            result = '\n'.join(str(count) + ') ' + str(admin[0]) for count, admin in enumerate(admins, 1))
    await callback.message.edit_text(text=f'Текущие админы:\n{result}',
                                     reply_markup=create_commands_keyboard('delete', 'add', marking=2))


@router.callback_query(F.data == 'yes', StateFilter(FSMBotStates.add_admin))
async def process_add_yes_command(callback: CallbackQuery, state: FSMContext) -> None:
    new_admins: list[str] = (await state.get_data())['new_admins']
    admins: list[tuple[int]] | None = await db.select_values(name_table='admins', columns='user_id')
    for admin_id in new_admins:
        if admins is None:
            await db.add_values_repetitive(name_table='admins', values=(int(admin_id),))
            admins = [(int(admin_id),)]
        else:
            admins.append((int(admin_id),))
            await db.add_values_repetitive(name_table='admins', values=(int(admin_id),))
    await state.update_data(admins=admins)
    await state.set_state(FSMBotStates.admin)
    result = '\n'.join(f'{i}) {str(word[0])}' for i, word in enumerate(admins, 1))
    await callback.message.edit_text(text=f'Текущие админы:\n{result}',
                                     reply_markup=create_commands_keyboard('delete', 'add', marking=2))


@router.callback_query(F.data == 'no', StateFilter(FSMBotStates.add_admin))
async def process_add_yes_command(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Введите id будущих админов бота:\n через запятую;\n через пробел;\n через перенос на новую строку.',
        reply_markup=create_commands_keyboard('back', marking=1))


@router.message(StateFilter(FSMBotStates.add_admin))
async def process_get_word_command(message: Message, state: FSMContext) -> None:
    new_admins: list[str] = message.text.replace('\n', ' ').replace(',',
                                                                    ' ').replace('"', "'").split()
    check: list[str] = []
    for word in new_admins:
        if word.strip() not in check:
            check.append(word.strip())
    await state.update_data(new_admins=check)
    text = '\n'.join(str(count) + ') ' + word for count, word in enumerate(check, 1))
    await message.answer(text=text,
                         reply_markup=create_commands_keyboard('no', 'yes', 'back', marking=(2, 1)))
