from aiogram import Bot, Dispatcher, executor, types
import random

def keyboard_no_yes():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='Да')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    keyboard.add(key_yes, key_no)
    return keyboard