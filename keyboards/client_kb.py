from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_enter_data() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/enter_data")],
    ], resize_keyboard=True, one_time_keyboard=True)


    return kb

def get_send_data() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/send_message")],
    ], resize_keyboard=True, one_time_keyboard=True)

    return kb

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))
