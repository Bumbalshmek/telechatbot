import telebot
from telebot import types
import config
import random
import time
import utils
import sqlite3
mevalues = []
state = 0
Channel_Name = '@roflersss'
class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM' + config.table_name ).fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM' + config.table_name + 'WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM' +config.table_name ).fetchall()
            return len(result)
    def new_row(self, func1res,func2res,func3res):
        with self.connection:
            self.cursor.execute('INSERT INTO '+ config.table_name +' ("Game_title","Pass_status","Grade") VALUES ("'+func1res +'", "'+func2res+'", "'+func3res+'")')
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['goback'])
def goback(message):
    global state
    state = 0
    mevalues.clear()
    bot.send_message(message.chat.id,'Вы вернулись в стартовое меню бота')
@bot.message_handler(commands=['games'])
def game(message):
    global state
    state = 1
    bot.send_message(message.chat.id, 'Введите название игры')
@bot.message_handler(func=lambda message: state == 1)
def r(message):
    mevalues.append(message.text)
    global state
    state = 2
    bot.send_message(message.chat.id, 'Введите вашу оценку ')
@bot.message_handler(func=lambda message: state == 2)
def rr(message):
    mevalues.append(message.text)
    global state
    state = 3
    bot.send_message(message.chat.id, 'Введите статус прохождения(пройдено или нет)')
@bot.message_handler(func=lambda message: state == 3)
def rrrr(message):
    mevalues.append(message.text)
    db_worker = SQLighter(config.database_name)
    db_worker.new_row(mevalues[0], mevalues[1], mevalues[2])
    db_worker.close()
    global state
    state = 0
    mevalues.clear()
    bot.send_message(message.chat.id,'В базу данных внесена новая игра')
    bot.send_message(Channel_Name, 'New rofl')
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, 'Вы запустили бота(список всех моих команд находится на клавиатуре)', reply_markup=keyboard1)
@bot.message_handler(content_types=["text"])
def send_text(message): # Название функции не играет никакой роли, в принципе
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id,'Хай зяблс')
    elif message.text.lower() == 'пока' :
        bot.send_message(message.chat.id, 'Пока')
    elif message.text.lower() == 'я саша' :
        a = random.randint(1,100)
        if a >= 50 :
            bot.send_message(message.chat.id, 'Мдааа.... Ну и рофлер')
        else:
            bot.send_message(message.chat.id, 'Саша...')
    else:
        bot.send_message(message.chat.id, 'Я пока не знаю как отвечать на это(я записываю то, что вы мне пишете)')
    f = open('logi.txt','a')
    f.write(time.ctime(time.time())+' '+message.text     + '\n')
    f.close()
@bot.message_handler(content_types='photo')
def compliments(message):
    a = random.randint(1, 100)
    if a <= 15:
        bot.send_message(message.chat.id, 'Неплохо Выглядишь')
    elif a<= 30:
        bot.send_message(message.chat.id, 'Выглядишь Изумительно')
    elif a<=45:
        bot.send_message(message.chat.id, 'Выглядишь Шикарно')
    elif a<=60:
        bot.send_message(message.chat.id, 'Выглядишь Умопомрачительно')
    elif a<=75:
        bot.send_message(message.chat.id, 'Выглядишь Невероятно')
    elif a<=90:
        bot.send_message(message.chat.id, 'Выглядишь Классно')
    else:
        bot.send_message(message.chat.id, 'Выглядишь Почти Также Как Мэйби Бэйби')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока','Я Саша','/games')
bot.polling(none_stop=True)