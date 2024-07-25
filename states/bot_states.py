from aiogram.fsm.state import (StatesGroup, State)


class FSMBotStates(StatesGroup):
    chats = State()
    words = State()
    del_chat = State()
    add_chat = State()
    del_word = State()
    add_word = State()