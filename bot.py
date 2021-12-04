import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('5012890665:AAHn6mn4P0uygxS0Kdbumfk9GR12BXgVUCQ')

user_dict = {}

class LIST:
    def __init__(self, msg):
        self.msg = msg
        self.del_pr = None


@bot.message_handler(commands=["start"])

def switch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("ДА")
    item2 = types.KeyboardButton("НЕТ")
    

    markup.add(item1, item2)

    chat_id = message.chat.id
    user_dict[chat_id] = LIST(message.text)
    msg = bot.send_message(chat_id, f'Готовы начать пробное тестирование?', reply_markup=markup)
    bot.register_next_step_handler(msg, add_pr)

def add_pr(message):
    if message.text == 'ДА':
        chat_id = message.chat.id
        user_dict[chat_id] = LIST(message.text)
        name = [message.text]
        a = telebot.types.ReplyKeyboardRemove()
        msg = bot.send_message(chat_id, f'Введите своё имя', reply_markup=a)
        bot.register_next_step_handler(msg, nameus)
        return name
    else:
        bot.send_message(message.chat.id, 'Хорошо, тогда продожим позже /start')
    
def nameus(message):

    connect = sqlite3.connect('bd.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login(
        id TEXT
    )""")
    
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login WHERE id = {people_id}")
    data = cursor.fetchone()
    
    try:
        if data is None:
            bot.send_message(message.chat.id, 'Спасибо)')
            chat_id = [message.chat.id]
            name = [message.text]
            cursor.execute("INSERT INTO login VALUES(?);", name)
            connect.commit()
        else:
            bot.send_message(message.chat.id, 'Вы уже зашли в систему)')
    except:
        pass



bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()