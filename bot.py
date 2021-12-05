import telebot
from telebot import types
import sqlite3
import time


bot = telebot.TeleBot('5012890665:AAHn6mn4P0uygxS0Kdbumfk9GR12BXgVUCQ')

user_dict = {}

class LIST:
    def __init__(self, msg):
        self.msg = msg
        self.del_pr = None


@bot.message_handler(commands=["start"])
def switch(message):
    connect = sqlite3.connect('bod.db')
    cursor = connect.cursor()

    try:
        cursor.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
    except Exception as e:
        print(repr(e))

    if not cursor.fetchone():
        try:
            cursor.execute("INSERT INTO users VALUES(?, ?);", (message.chat.id, message.from_user.username))
            connect.commit()

            bot.send_message(message.chat.id, 'Welcome')
        except:
            pass
    else:
        bot.send_message(message.chat.id, 'Вы уже есть в системе')

    if connect:
        connect.close()


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("ДА")
    item2 = types.KeyboardButton("НЕТ")
    

    markup.add(item1, item2)

    chat_id = message.chat.id
    user_dict[chat_id] = LIST(message.text)
    msg = bot.send_message(chat_id, f'Компьютерные игры это круто?', reply_markup=markup)
    bot.register_next_step_handler(msg, task1)

def task1(message):
    connect = sqlite3.connect('bod.db')
    cursor = connect.cursor()

    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Такой же где и везде")
    item2 = types.KeyboardButton("Сгенерированный в спец. программе")
    

    markup2.add(item1, item2)

    if message.text == "ДА":
        try:
            chat_id = message.chat.id
            user_dict[chat_id] = LIST(message.text)
            cursor.execute("INSERT INTO task VALUES(?, ?);", (message.from_user.username ,"true"))
            connect.commit()
            
            msg = bot.send_message(chat_id, f'Какой пароль лучше использовать для входа в компьютер?', reply_markup=markup2)
            bot.register_next_step_handler(msg, task2)
        except:
            pass
    elif message.text == "НЕТ":
        try:
            chat_id = message.chat.id
            user_dict[chat_id] = LIST(message.text)
            cursor.execute("INSERT INTO task VALUES(?, ?);", (message.from_user.username, ""))
            connect.commit()
            msg = bot.send_message(chat_id, f'Какой пароль лучше использовать для входа в компьютер?', reply_markup=markup2)
            bot.register_next_step_handler(msg, task2)
        except:
            pass

def task2(message):
    connect = sqlite3.connect('bod.db')
    cursor = connect.cursor()


    if message.text == "Сгенерированный в спец. программе":
        try:
            chat_id = message.chat.id
            user_dict[chat_id] = LIST(message.text)
            cursor.execute("INSERT INTO task2 VALUES(?, ?);", (message.from_user.username ,"true"))
            connect.commit()
            a = telebot.types.ReplyKeyboardRemove()
            msg = bot.send_message(chat_id, f'Перейти к итогам?', reply_markup=a)
            bot.register_next_step_handler(msg, itog)
        except:
            pass
    elif message.text == "Такой же где и везде":
        try:
            chat_id = message.chat.id
            user_dict[chat_id] = LIST(message.text)
            cursor.execute("INSERT INTO task2 VALUES(?, ?);", (message.from_user.username, ""))
            connect.commit()
            a = telebot.types.ReplyKeyboardRemove()
            msg = bot.send_message(chat_id, f'Перейти к итогам?', reply_markup=a)
            bot.register_next_step_handler(msg, itog)
        except:
            pass

def itog(message):
    n = 3
    for i in range(3):
        n-=1
        a = message.from_user.username
        connect = sqlite3.connect('bod.db')
        cursor = connect.cursor()
        idd = (a,)
        cursor.execute(f"SELECT * FROM task WHERE user = ?",idd)
        data=cursor.fetchone()
        if data is None:
            pass
        else:
            an = ('true',)
            cursor.execute(f"SELECT * FROM task WHERE answer = ?",an)
            data=cursor.fetchone()
            if data is None:
                bot.send_message(message.chat.id,"Статья 1")
                time.sleep(3)
                cursor.execute(f"SELECT * FROM task2 WHERE user = ?",idd)
                data=cursor.fetchone()
                if data is None:
                    pass
                else:
                    cursor.execute(f"SELECT * FROM task2 WHERE answer = ?",an)
                    data=cursor.fetchone()
                    if data is None:
                        bot.send_message(message.chat.id,"Статья 2")
                        time.sleep(3)
                    else:
                        pass
            else:
                cursor.execute(f"SELECT * FROM task2 WHERE user = ?",idd)
                data=cursor.fetchone()
                if data is None:
                    pass
                else:
                    cursor.execute(f"SELECT * FROM task2 WHERE answer = ?",an)
                    data=cursor.fetchone()
                    if data is None:
                        bot.send_message(message.chat.id,"Статья 2")
                        time.sleep(3)
                    else:
                        pass
    



# def itog(message):
#     a = 0
#     connect = sqlite3.connect('bod.db')
#     cursor = connect.cursor()
    
#     cursor.execute("INSERT INTO itog VALUES(?, ?);", (message.from_user.username , a))
#     connect.commit()

#     cursor.execute(f"SELECT * FROM task WHERE user = (true)")
#     data=cursor.fetchone()
#     if data is None:
#         a=1
#         cursor.execute(f"SELECT * FROM task WHERE user = (true)")
#         data=cursor.fetchone()
#         if data is None:
#             a=2
#             cursor.execute("INSERT INTO itog VALUES(?, ?);", (message.from_user.username , a))
#             connect.commit()
#             bot.send_message(message.chat.id, a)
#         else:
#             cursor.execute("INSERT INTO itog VALUES(?, ?);", (message.from_user.username , a))
#             connect.commit()
#             bot.send_message(message.chat.id, a)
#     else:
#         cursor.execute(f"SELECT * FROM task2 WHERE answer = true")
#         data=cursor.fetchone()
#         if data is None:
#             a=1
#             cursor.execute("UPDATE INTO itog VALUES(?, ?);", (message.from_user.username , a))
#             connect.commit()
#             bot.send_message(message.chat.id, a + "/10")
#         else:
#             cursor.execute("UPDATE INTO itog VALUES(?, ?);", (message.from_user.username , a))
#             connect.commit()
#             bot.send_message(message.chat.id, a + "/10")

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()