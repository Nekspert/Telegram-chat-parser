from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)


def create_commands_keyboard(*args, marking: int | tuple[int]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for button in args:
        button: str
        if '_start' in button:
            buttons.append(
                InlineKeyboardButton(text=button.replace('start', '').replace('_', ' '), callback_data=button))
        elif '_menu' in button:
            buttons.append(
                InlineKeyboardButton(text=button.replace('menu', '').replace('_', ' '), callback_data=button))
        else:
            buttons.append(InlineKeyboardButton(text=button.replace('_', ' '), callback_data=button))
    if isinstance(marking, int):
        kb.row(*buttons, width=marking)
        return kb.as_markup(one_time_keyboard=True, resize_keyboard=True)

    kb.add(*buttons)
    if isinstance(marking, tuple):
        res = []
        for value in marking:
            res.append(value)
        kb.adjust(*res)
    else:
        kb.adjust(*marking)
    return kb.as_markup(one_time_keyboard=True, resize_keyboard=True)


def create_chats_keyboard(*args, flag: int = 0):
    kb = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    count = 0
    for button in args:
        count += 1
        buttons.append(InlineKeyboardButton(text=button['title'], callback_data=str(button['id'])))
    buttons.append(InlineKeyboardButton(text='<<', callback_data=f'backward_{flag}'))
    buttons.append(InlineKeyboardButton(text='>>', callback_data=f'forward_{flag}'))
    buttons.append(InlineKeyboardButton(text='back', callback_data='back'))
    kb.add(*buttons)
    result: list[int] = [1 for _ in range(count)]
    result.append(2)
    result.append(1)
    kb.adjust(*result)
    return kb.as_markup(one_time_keyboard=True, resize_keyboard=True)


def create_admin_keyboard(*args, flag: int = 0):
    kb = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    count = 0
    for button in args:
        count += 1
        buttons.append(InlineKeyboardButton(text=str(button[0]), callback_data=str(button[0])))
    buttons.append(InlineKeyboardButton(text='<<', callback_data=f'backward_{flag}'))
    buttons.append(InlineKeyboardButton(text='>>', callback_data=f'forward_{flag}'))
    buttons.append(InlineKeyboardButton(text='back', callback_data='back'))
    kb.add(*buttons)
    result: list[int] = [1 for _ in range(count)]
    result.append(2)
    result.append(1)
    kb.adjust(*result)
    return kb.as_markup(one_time_keyboard=True, resize_keyboard=True)


def create_words_keyboard(*args, flag: int = 0):
    kb = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    count = 0
    for button in args:
        count += 1
        buttons.append(InlineKeyboardButton(text=button[0], callback_data=button[0]))
    buttons.append(InlineKeyboardButton(text='<<', callback_data=f'backward_{flag}'))
    buttons.append(InlineKeyboardButton(text='>>', callback_data=f'forward_{flag}'))
    buttons.append(InlineKeyboardButton(text='back', callback_data='back'))
    kb.add(*buttons)
    result: list[int] = [1 for _ in range(count)]
    result.append(2)
    result.append(1)
    kb.adjust(*result)
    return kb.as_markup(one_time_keyboard=True, resize_keyboard=True)
