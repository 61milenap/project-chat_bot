from telebot import types
import telebot
import sqlite3
from pprint import pp, pprint

with open("config.txt") as config:
    token = config.readline().strip()

db = sqlite3.connect("data.db")
c = db.cursor()

c.execute("""CREATE TABLE users_info (
     id text,
     score integer,
     temp integer,
     num integer,
     activity integer,
     first_name text,
     last_name text
 )""")
# res = c.execute("SELECT id FROM users_info").fetchall()
# text = f"Бот заработает в течение 5 минут!"
# bot = telebot.TeleBot(token)
# for user in res:
#   try:
#       bot.send_message(user[0], text, parse_mode="html")
#    except Exception:
#        print("ТЕБЯ ГИГАНТ ЗАБЛОКИРОВАЛ, ОБИДНО")
# c.execute("UPDATE users_info SET temp = ?, score = ?, num = ?, activity = ?", (0, 0, -1, 0))
# db.commit()
# res = c.execute("SELECT * FROM users_info").fetchall()
# pprint(len(res))
db.commit()
db.close()
