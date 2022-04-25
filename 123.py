from telebot import types
import telebot
import sqlite3
import random
import time
import traceback
import threading
from get_message import send_message

token = '5356313952:AAGoUZCC1MnWZBwIZshXNdJ8_67whebrH4M'
lock = threading.Lock()
with open("dictionary/words.txt") as f_words:
    words = f_words.read().split("\n")

with open("dictionary/blackWords.txt") as f_blackWords:
    blackWords = f_blackWords.read().split("\n")

bot = telebot.TeleBot(token)

db = sqlite3.connect("data.db", check_same_thread=False)

# Create Cursor for db
cur = db.cursor()



def get_task(words_d, blackWords_d):
    s_words = set()
    s_black = set()
    while len(s_words) != 3:
        num = random.randrange(0, len(words_d) - 1)
        s_words.add(words[num])
    num = random.randrange(0, len(blackWords_d) - 1)
    s_black.add(blackWords[num])
    return s_words, s_black

def get_variant():
    s_words, s_black = get_task(words, blackWords)
    s_words = list(s_words)
    s_black = list(s_black)
    numWright = random.randrange(0, 3)
    answers = [''] * 4
    answers[numWright] = s_black[0]
    count = 0
    for j in s_words:
        if answers[count] == '':
            answers[count] = j
        else:
            count += 1
            answers[count] = j
        count += 1
    text = ""
    for j in range(len(answers)):
        text += f"{j + 1}) {answers[j]} \n"
    return text, numWright

def get_variant():
    s_words, s_black = get_task(words, blackWords)
    s_words = list(s_words)
    s_black = list(s_black)
    numWright = random.randrange(0, 3)
    answers = [''] * 4
    answers[numWright] = s_black[0]
    count = 0
    for j in s_words:
        if answers[count] == '':
            answers[count] = j
        else:
            count += 1
            answers[count] = j
        count += 1
    text = ""
    for j in range(len(answers)):
        text += f"{j + 1}) {answers[j]} \n"
    return text, numWright


def find_in_data(id_user):
    global cur
    with lock:
        res = cur.execute("SELECT * FROM users_info WHERE id = ?", (str(id_user), )).fetchall()

    return res != []

def keyboard_no_yes():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='Да')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    keyboard.add(key_yes, key_no)
    return keyboard

def keyboard_answer():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    key_1 = types.InlineKeyboardButton(text='1', callback_data='1')
    key_2 = types.InlineKeyboardButton(text='2', callback_data='2')
    keyboard.add(key_1, key_2)
    key_3 = types.InlineKeyboardButton(text='3', callback_data='3')
    key_4 = types.InlineKeyboardButton(text='4', callback_data='4')
    keyboard.add(key_3, key_4)
    return keyboard
