from aiogram.utils.keyboard import (ReplyKeyboardBuilder, InlineKeyboardBuilder)
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)

from lexicon.lexicon_ru import LEXICON


def create_inline_keyboard(*args, marking: int | tuple[int]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if isinstance(args[0], list):
        if len(args) > 1:
            for button in args[0]:
                if button in LEXICON:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=LEXICON[button]))
                else:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=str(button)))
            for button in args[1:]:
                if button in LEXICON:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=LEXICON[button]))
                else:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=str(button)))
        else:
            for button in args[0]:
                if button in LEXICON:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=LEXICON[button]))
                else:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=str(button)))
    else:
        for button in args:
            if button in LEXICON:
                buttons.append(InlineKeyboardButton(text=str(button), callback_data=LEXICON[button]))
            else:
                buttons.append(InlineKeyboardButton(text=str(button), callback_data=str(button)))
    if isinstance(marking, int):
        kb.row(*buttons, width=marking)
        return kb.as_markup(one_time_keyboard=True, resize_keyboard=True)
    kb.add(*buttons)
    if isinstance(marking[0], tuple):
        res = []
        for value in marking[0]:
            res.append(value)
        for value in marking[1:]:
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

