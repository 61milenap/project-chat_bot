import os
import time
from aiogram import Bot, Dispatcher, executor, types
import pymysql




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