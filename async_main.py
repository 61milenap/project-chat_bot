from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import random
import time
from get_message import send_message
#from pprint import pprint

with open("config.txt") as config:
    token = config.readline().strip()

with open("dictionary/words.txt", encoding="utf-8") as f_words:
    words = f_words.read().split("\n")

with open("dictionary/blackWords.txt", encoding="utf-8") as f_blackWords:
    blackWords = f_blackWords.read().split("\n")

bot = Bot(token=token)
dp = Dispatcher(bot)
db = sqlite3.connect("data.db")

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


def find_in_data(id_user):
    global cur
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

@dp.message_handler(commands="start")
async def start(message: types.Message):
    if not find_in_data(message.from_user.id):
        id_user = message.from_user.id
        score = 0
        temp = 0
        num = -1
        activity = 0
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        cur.execute("INSERT INTO users_info VALUES (?, ?, ?, ?, ?, ?, ?)", (str(id_user), score, temp, num, activity, first_name, last_name))
        send_message(f"{first_name} зарегистрировался в вашем боте!")
        db.commit()
    activity = 0
    temp = 0
    num = -1
    cur.execute("UPDATE users_info SET activity = ?, temp = ?, num = ? WHERE id = ?", (activity, temp, num, message.from_user.id))
    db.commit()
    text = f"🖐🏾 Привет, <b>{message.from_user.first_name}</b>.\nНачать тренировку?"
    keyboard = keyboard_no_yes()
    await message.answer(text, parse_mode="html", reply_markup=keyboard)


@dp.message_handler(commands="record")
async def record(message: types.Message):
    if not find_in_data(str(message.from_user.id)):
        text = f"Вас нет в базе данных! Нажмите на /start, {message.from_user.id.first_name}"
        await message.answer(text, parse_mode="html")
        return
    record = int(cur.execute("SELECT score FROM users_info WHERE id = ?", (str(message.from_user.id), )).fetchall()[0][0])
    text = f"🏋🏿‍♀️ Ваш рекорд: {record}"
    await message.answer(text, parse_mode="html")


@dp.message_handler(commands="users")
async def users(message: types.Message):
    res = cur.execute("SELECT * FROM users_info").fetchall() 
    text = f"📊 Количество пользователей: {len(res)}"
    await message.answer(text, parse_mode="html")


@dp.message_handler(commands="update")
async def update(message: types.Message):
    cur.execute("UPDATE users_info SET first_name = ?, last_name = ? WHERE id = ?", (message.from_user.first_name, message.from_user.last_name, message.from_user.id))
    db.commit()
    text = f"😉 Имя пользователя обновлено!"
    await message.answer(text, parse_mode="html")


@dp.message_handler(commands="leaderboard")
async def leaderboard(message: types.Message):
    leader_board = cur.execute("SELECT first_name, last_name, score FROM users_info ORDER BY score DESC").fetchmany(10)
    text = "🏆 Таблица лидеров:\n\n"
    num = 0
    for j in leader_board:
        num += 1
        first_name, last_name, score = j
        if num == 1:
            text += "🥇 "
        elif num == 2:
            text += "🥈 "
        elif num == 3:
            text += "🥉 "
        else:
            text += f" {num}. "
        if last_name != None:
            text += f"{first_name} {last_name} — {score}\n"
        else:
            text += f"{first_name} — {score}\n"
    await message.answer(text, parse_mode="html")

@dp.message_handler()
async def training(message: types.Message):
    if not find_in_data(str(message.from_user.id)):
        text = f"Вас нет в базе данных! Нажмите на /start, {message.from_user.first_name}"
        await message.answer(text, parse_mode="html")
        return
    activity = int(cur.execute("SELECT activity FROM users_info WHERE id = ?", (str(message.from_user.id), )).fetchall()[0][0])
    if activity:
        activity = 0
        num = int(cur.execute("SELECT num FROM users_info WHERE id = ?", (str(message.from_user.id), )).fetchall()[0][0])
        temp = int(cur.execute("SELECT temp FROM users_info WHERE id = ?", (str(message.from_user.id), )).fetchall()[0][0])
        score = int(cur.execute("SELECT score FROM users_info WHERE id = ?", (str(message.from_user.id), )).fetchall()[0][0])
        if any(message.text == x for x in ["1", "2", "3", "4"]):
            if message.text == str(num + 1):
                temp += 1
                if temp > score:
                    score = temp
                num = -1
                text = f"✅ <b>Верно!</b> Желаете ли вы продолжить дальше?\n<b>score:{temp}</b>"
                keyboard = keyboard_no_yes()
                cur.execute("UPDATE users_info SET activity = ?, num = ?, temp = ?, score = ? WHERE id = ?", (activity, num, temp, score, str(message.from_user.id)))
                db.commit()
                await message.answer(text, parse_mode="html", reply_markup=keyboard)

            else:
                if temp > score:
                    score = temp
                temp = 0
                text = f"❌ <b>НЕВЕРНО! </b>\n Желаете ли вы начать заново?"
                keyboard = keyboard_no_yes()
                num = -1
                cur.execute("UPDATE users_info SET activity = ?, num = ?, temp = ?, score = ? WHERE id = ?", (activity, num, temp, score, str(message.from_user.id)))
                db.commit()
                await message.answer(text, parse_mode="html", reply_markup=keyboard)
        else:
            keyboard = keyboard_answer()
            await message.answer(
                         f"😡 Я тебя не понимаю, дружище. Соберитесь, <b>{message.from_user.first_name}</b>",
                         parse_mode="html", reply_markup=keyboard)
    elif message.text == "Да" or message.text == "Далее" and not activity:
        activity = 1
        keyboard = keyboard_answer()
        text, num = get_variant()
        question = "🕵🏿 Укажите вариант ответа, где ударение выставлено <b>неверно</b>\n"
        text = question + text
        cur.execute("UPDATE users_info SET activity = ?, num = ? WHERE id = ?", (activity, num, str(message.from_user.id)))
        db.commit()
        await message.answer(text, parse_mode="html", reply_markup=keyboard)
    elif message.text == "Нет":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        key_start = types.InlineKeyboardButton(text='/start', callback_data='/start')
        keyboard.add(key_start)
        text = "😳 Хорошо, но задумайся над пословицей:\nШевели раньше <b>мозгами</b>, а то поплатишься <b>щеками</b>."
        await message.answer(text, parse_mode="html", reply_markup=keyboard)
    else:
        await message.answer(
                         f"😡 Я тебя не понимаю, дружище. Соберитесь, <b>{message.from_user.first_name}</b>",
                         parse_mode="html")


#while True:
#    try:
executor.start_polling(dp, skip_updates=True)
#    except Exception as e:
#        send_message(e)
#        time.sleep(15)
db.close()