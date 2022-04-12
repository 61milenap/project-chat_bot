import os
import time
from aiogram import Bot, Dispatcher, executor, types
import pymysql


FAQ = ""
full_info = [[] for _ in range(3)]
for i in range(3):
    with open(f"data/{i + 1}.txt", "r") as file:
        f = file.read()
    for j in f.split("&\n"):
        if (len(j) < 2):
            continue
        info = j.split("#\n")
        text = info[0].strip()
        answer = info[1].strip()
        full_info[i].append([text, answer])
with open("FAQ.txt", "r") as file:
    FAQ = file.read()

# подключение к базе данных и к боту
TOKEN = os.environ.get('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = pymysql.connect(
    host='',
    user='standart',
    password='1',
    database='ege_russian_db',
    cursorclass=pymysql.cursors.DictCursor)
cur = db.cursor()


@dp.message_handler(commands="FAQ")
async def faq(message: types.Message):
    await message.answer(FAQ, parse_mode="html")


def find_in_data(id_user):
    cur.execute(f"SELECT * FROM users WHERE id = '{id_user}'")
    res = cur.fetchall()
    return res != ()

def total():
    cur.execute("SELECT * from stats")
    info = cur.fetchall()[0]
    counter = int(info["counter"])
    counter += 1
    cur.execute(f"UPDATE `stats` SET counter = '{counter}'")
    db.commit()
    return counter

def check_response(id_user, answer):
    cur.execute(f"SELECT right_ans, wrong_ans FROM `users` WHERE id = '{id_user}'")
    info = cur.fetchall()[0]
    right_ans = int(info["right_ans"])
    wrong_ans = int(info["wrong_ans"])
    if answer:
        right_ans += 1
    else:
        wrong_ans += 1
    cur.execute(f"UPDATE `users` SET right_ans = '{right_ans}', wrong_ans = '{wrong_ans}' WHERE id = '{id_user}'")
    db.commit()
