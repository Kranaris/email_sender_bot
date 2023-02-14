from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_enter_data() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/ввести_показания")],
    ], resize_keyboard=True, one_time_keyboard=True)


    return kb

def get_send_data() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("/отправить_показания")],
    ], resize_keyboard=True, one_time_keyboard=True)