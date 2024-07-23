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


def create_reply_keyboard(*args, marking: int | tuple[int]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []
    for button in args:
        if button in LEXICON:
            buttons.append(KeyboardButton(text=LEXICON[button]))
        else:
            buttons.append(KeyboardButton(text=str(button)))
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


def create_arrows_keyboard(*args, marking: int | tuple[int] | tuple[tuple[int] | int]) -> InlineKeyboardMarkup:
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
                    if str(button).startswith('>>') or str(button).startswith('<<'):
                        buttons.append(InlineKeyboardButton(text=str(button).split('_')[0], callback_data=str(button)))
                    else:
                        buttons.append(InlineKeyboardButton(text=str(button), callback_data=str(button)))
        else:
            for button in args[0]:
                if button in LEXICON:
                    buttons.append(InlineKeyboardButton(text=str(button), callback_data=LEXICON[button]))
                else:
                    if str(button).startswith('>>') or str(button).startswith('<<'):
                        buttons.append(InlineKeyboardButton(text=str(button).split('_')[0], callback_data=str(button)))
                    else:
                        buttons.append(InlineKeyboardButton(text=str(button), callback_data=str(button)))
    else:
        for button in args:
            if button in LEXICON:
                buttons.append(InlineKeyboardButton(text=str(button), callback_data=LEXICON[button]))
            else:
                if str(button).startswith('>>') or str(button).startswith('<<'):
                    buttons.append(InlineKeyboardButton(text=str(button).split('_')[0], callback_data=str(button)))
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

