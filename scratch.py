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
    def check_state(self,user_id):
        """Проверяет состояние пользователя"""
        with self.connection:
            resultt = self.cursor.execute('SELECT count(state)>0 FROM '+ config.table_name +' WHERE user_id = "'+str(user_id)+'"').fetchall()
            return resultt
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
    def send_info(self,user_data_list):
        """Отправление полной анкеты в базу данных"""
        with self.connection:
            sender = self.cursor.execute('UPDATE ' + config.table_name + ' SET uuser_name = "'+str(user_data_list[1])+'", sex = '+str(user_data_list[2])+',' 
            'age = '+str(user_data_list[3])+', city = "'+user_data_list[4]+'", lookingfor = '+str(user_data_list[5])+ ', opisaniye = "'+user_data_list[6]+'"'
            ', image = "'+str(user_data_list[7])+'", state = '+str(user_data_list[8])+' WHERE user_id  = "'+ str(user_data_list[0]) +'"')
        return sender
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['test'])
def chenit(message):
    db_worker = SQLighter(config.database_name)
    var = db_worker.check_row(message.chat.id)
    varr = db_worker.check_state(message.chat.id)
    if var[0] == (1,) and varr[0] == (1,):
        bot.send_message(message.chat.id,'id exists, your profile saved')
    elif var[0] == (1,) :
        bot.send_message(message.chat.id,'id exists, but your profile is not completed enter name')
        Ud.append(db_worker.show_info(message.chat.id))
        print(db_worker.show_info(message.chat.id))
        for i in range(len(Ud)):
            Ud[i-1][0] = list(Ud[i-1][0])
        for i in range(len(Ud)):
            if Ud[i-1][0][0] == message.chat.id:
                Ud[i-1][0][8] = 1
    else :
        bot.send_message(message.chat.id,'id not exists and will be added enter your name')
        db_worker.new_row(message.chat.id)
        Ud.append(db_worker.show_info(message.chat.id))
        print(db_worker.show_info(message.chat.id))
        for i in range(len(Ud)):
            Ud[i-1][0] = list(Ud[i-1][0])
        for i in range(len(Ud)):
            if Ud[i-1][0][0] == message.chat.id:
                Ud[i-1][0][8] = 1
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, 'Вы запустили бота(список всех моих команд находится на клавиатуре)', reply_markup=keyboard1)
@bot.message_handler(commands=['showmyid'])
def showid(message):
    bot.send_message(message.chat.id, message.chat.id)
@bot.message_handler(content_types=["text"])
def send_text(message): # Название функции не играет никакой роли, в принципе
    if len(Ud) > 0 :
        for i in range(len(Ud)):
            #name block
            if Ud[i-1][0][8] == 1 and Ud[i-1][0][0] == message.chat.id:
                Ud[i-1][0][1] = message.text
                Ud[i-1][0][8] = 2
                bot.send_message(message.chat.id, 'enter your sex male/female')
            # gender block
            elif Ud[i-1][0][8] == 2 and Ud[i-1][0][0] == message.chat.id:
                if message.text.lower() == 'male':
                    Ud[i - 1][0][2] = 1
                    Ud[i - 1][0][8] = 3
                    bot.send_message(message.chat.id, 'enter your age')
                elif message.text.lower() == 'female':
                    Ud[i - 1][0][2] = 0
                    Ud[i - 1][0][8] = 3
                    bot.send_message(message.chat.id, 'enter your age')
                else :
                    bot.send_message(message.chat.id,'please enter correct answer')
            #age block
            elif Ud[i - 1][0][8] == 3 and Ud[i-1][0][0] == message.chat.id :
                if int(message.text) > 10 and int(message.text) < 99:
                    Ud[i - 1][0][3] = message.text
                    Ud[i - 1][0][8] = 4
                    bot.send_message(message.chat.id, 'Where you live')
                else:
                    bot.send_message(message.chat.id,'incorrent answer')
            #city block
            elif Ud[i - 1][0][8] == 4 and Ud[i-1][0][0] == message.chat.id:
                if type(message.text) == str:
                    Ud[i - 1][0][4] = message.text
                    Ud[i - 1][0][8] = 5
                    bot.send_message(message.chat.id,'Who Are You Looking For?(male/female/everyone)')
                else:
                    bot.send_message(message.chat.id,'incorrect answer')
            #lookingfor block
            elif Ud[i - 1][0][8] == 5 and Ud[i-1][0][0] == message.chat.id:
                if message.text.lower() == 'male':
                    Ud[i-1][0][5] = 1
                    Ud[i-1][0][8] = 6
                    bot.send_message(message.chat.id, 'now write a little about yourself')
                elif message.text.lower() == 'female':
                    Ud[i-1][0][5] = 2
                    Ud[i-1][0][8] = 6
                    bot.send_message(message.chat.id, 'now write a little about yourself')
                elif message.text.lower() == 'everyone':
                    Ud[i-1][0][5] = 3
                    Ud[i-1][0][8] = 6
                    bot.send_message(message.chat.id, 'now write a little about yourself')
                else:
                    bot.send_message(message.chat.id,'incorrect answer')
            #self description block
            elif Ud[i - 1][0][8] == 6 and Ud[i-1][0][0] == message.chat.id:
                Ud[i - 1][0][6] = message.text
                Ud[i - 1][0][8] = 7
                bot.send_message(message.chat.id, 'send me your profile pic photo')
                print(Ud)
    else:
        bot.send_message(message.chat.id,'please type /test')
    f = open('logi.txt','a')
    f.write(time.ctime(time.time())+' '+message.text     + '\n')
    f.close()
@bot.message_handler(content_types='photo')
def profilepic(message):
    for i in range (len(Ud)):
        if Ud[i-1][0][8] == 7 and Ud[i-1][0][0] == message.chat.id:
            Ud[i-1][0][7] = message.photo[0].file_id
            db_worker = SQLighter(config.database_name)
            db_worker.send_info(Ud[i - 1][0])
            bot.send_message(message.chat.id,'Your profile:',disable_notification = True)
            bot.send_photo(message.chat.id, Ud[i-1][0][7], caption= Ud[i-1][0][1]+', '+Ud[i-1][0][3]+', '+Ud[i-1][0][4]+'\n'+Ud[i-1][0][6])
            for k in range (len(Ud)):
                if Ud[k-1][0][0] == message.chat.id:
                    Ud.pop(k-1)

            bot.send_message(Channel_Name, 'New rofl')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока','Я Саша','/showmyid')
bot.polling(none_stop=True)