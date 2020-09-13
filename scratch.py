import telebot
from telebot import types
import config
import random
import time
import utils
import sqlite3
mevalues = []
user_state = 0
Ud = []
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

    def new_row(self, user_id):
        """Добавление новой строки в таблицу(все ячейки кроме айди = Null)"""
        with self.connection:
            self.cursor.execute('INSERT INTO '+ config.table_name +' ("user_id") VALUES ("'+str(user_id)+'")')

    def check_row(self,user_id):
        """Проверяет таблицу на наличие определенного айди в ней"""
        with self.connection:
            result = self.cursor.execute('SELECT count(user_id)>0 FROM '+ config.table_name +' WHERE user_id = "'+str(user_id)+'"').fetchall()
            return result

    def show_info(self,user_id):
        """Выдача данных из одной строки таблицы списком"""
        with self.connection:
            information = self.cursor.execute('SELECT * FROM ' + config.table_name +' WHERE user_id = "'+str(user_id)+ '"').fetchall()
            return information

    def add_to_row(self,text,user_id):
        """ Добавление контента в определенную строку таблицы """
        with self.connection:
            roflinochka = self.cursor.execute('UPDATE ' + config.table_name + ' SET lookingfor = '+text+' WHERE user_id  = "'+str(user_id)+'"')
            return roflinochka
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['test'])
def chenit(message):
    db_worker = SQLighter(config.database_name)
    var = db_worker.check_row(message.chat.id)
    if var[0] == (1,):
        bot.send_message(message.chat.id,'id exists, enter your age')
        Ud.append(db_worker.show_info(message.chat.id))
        print(db_worker.show_info(message.chat.id))
        for i in range(len(Ud)):
            Ud[i-1][0] = list(Ud[i-1][0])
        for i in range(len(Ud)):
            if Ud[i-1][0][0] == message.chat.id:
                Ud[i-1][0][7] = 1
    else :
        bot.send_message(message.chat.id,'id not exists and will be added')
        db_worker.new_row(message.chat.id)
@bot.message_handler(commands=['goback'])
def goback(message):
    global user_state
    user_state = message.chat.id
    mevalues.clear()
    bot.send_message(message.chat.id,'Вы вернулись в стартовое меню бота')
@bot.message_handler(commands=['games'])
def game(message):
    global user_state
    user_state = message.chat.id + 1
    bot.send_message(message.chat.id, 'Введите название игры')
@bot.message_handler(func=lambda message: user_state - message.chat.id == 1)
def r(message):
    mevalues.append(message.text)
    global user_state
    user_state = message.chat.id + 2
    bot.send_message(message.chat.id, 'Введите статус прохождения(пройдено или нет)')
@bot.message_handler(func=lambda message: user_state - message.chat.id == 2)
def rr(message):
    mevalues.append(message.text)
    global user_state
    user_state = message.chat.id + 3
    bot.send_message(message.chat.id, 'Введите оценку')
@bot.message_handler(func=lambda message: user_state - message.chat.id == 3)
def rrrr(message):
    mevalues.append(message.text)
    db_worker = SQLighter(config.database_name)
    db_worker.new_row(mevalues[0], mevalues[1], mevalues[2])
    db_worker.close()
    global user_state
    user_state = 0
    mevalues.clear()
    bot.send_message(message.chat.id,'В базу данных внесена новая игра')
    bot.send_message(Channel_Name, 'New rofl')
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, 'Вы запустили бота(список всех моих команд находится на клавиатуре)', reply_markup=keyboard1)
@bot.message_handler(commands=['showmyid'])
def showid(message):
    bot.send_message(message.chat.id, message.chat.id)
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
keyboard1.row('Привет', 'Пока','Я Саша','/showmyid')
bot.polling(none_stop=True)