import telebot
import config
import random
import sqlite3
import cherrypy
profiles_dict = dict()
Ud_dict = dict()
Ud = []
matches_dict = dict()
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
            return self.cursor.execute('SELECT * FROM ' + config.table_name + ' WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM ' +config.table_name ).fetchall()
            return len(result)

    def new_row(self, user_id):
        """Добавление новой строки в таблицу(все ячейки кроме айди = Null)"""
        with self.connection:
            self.cursor.execute('INSERT INTO '+ config.table_name +' ("user_id") VALUES ("'+str(user_id)+'")')

    def gender_check(self,user_id):
        """Проверка пола пользователя"""
        with self.connection:
            gender = self.cursor.execute('SELECT sex FROM '+ config.table_name +' WHERE user_id = "'+str(user_id)+'"').fetchall()
            return gender

    def check_row(self,user_id):
        """Проверяет таблицу на наличие определенного айди в ней"""
        with self.connection:
            result = self.cursor.execute('SELECT count(user_id)>0 FROM '+ config.table_name +' WHERE user_id = "'+str(user_id)+'"').fetchall()
            return result

    def check_state(self,user_id):
        """Проверяет состояние пользователя"""
        with self.connection:
            resultt = self.cursor.execute('SELECT user_id, state FROM '+ config.table_name +' WHERE user_id = "'+str(user_id)+'"').fetchall()
            return resultt

    def show_info(self,user_id):
        """Выдача данных из одной строки таблицы списком"""
        with self.connection:
            information = self.cursor.execute('SELECT * FROM ' + config.table_name +' WHERE user_id = "'+str(user_id)+ '"').fetchall()
            information[0] = list(information[0])
            return information
    def state_update(self,user_id,new_state):
        with self.connection:
            self.cursor.execute('UPDATE '+ config.table_name + ' SET state = '+str(new_state)+' WHERE user_id  = "'+str(user_id)+'"')
    def preference_check(self,user_id):
        """Проверка предпочтений пользователя"""
        with self.connection:
            preference = self.cursor.execute('SELECT lookingfor FROM '+ config.table_name+' WHERE user_id = "'+str(user_id)+'"').fetchall()
            return preference
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
            ', image = "'+str(user_data_list[7])+'", state = '+str(user_data_list[8])+', username = "'+str(user_data_list[9])+ '" WHERE user_id  = "'+ str(user_data_list[0]) +'"')
        return sender
    def id_list(self,user_id):
        with self.connection:
            ids = self.cursor.execute('SELECT user_id FROM '+config.table_name+' WHERE NOT user_id = "'+str(user_id)+'" AND NOT state = 1 AND NOT state = 15').fetchall()
            return ids
    def id_list_full(self):
        with self.connection:
            ids = self.cursor.execute('SELECT user_id FROM '+config.table_name+'').fetchall()
            return ids
    def create_match(self,user_id,matched_id):
        with self.connection:
            if self.cursor.execute('SELECT COUNT(*)>0 FROM matches WHERE user_id = "' + str(user_id) + '" AND match_user_id = "' +str(matched_id)+ '"').fetchall()[0] == (0,):
                self.cursor.execute('INSERT INTO matches ("user_id","match_user_id") VALUES (' + str(user_id) + ',' + str(
                matched_id) +')')
            else:
                pass
    def create_match_and_text(self,user_id,matched_id,text):
        with self.connection:
            if self.cursor.execute(
                    'SELECT COUNT(*)>0 FROM matches WHERE user_id = "' + str(user_id) + '" AND match_user_id = "' + str(
                            matched_id) + '"').fetchall()[0] == (0,):
                self.cursor.execute('INSERT INTO matches ("user_id","match_user_id","reaction") VALUES ('+str(user_id)+','+str(matched_id)+',"'+str(text)+'")')
            else:
                pass
    def check_text(self,user_id,matched_id):
        with self.connection:
            if (self.cursor.execute('SELECT reaction FROM matches WHERE user_id = '+str(user_id)+' AND match_user_id = '+str(matched_id)+'').fetchall()[0][0]) == None:
                k = 0
            else:
                k = (self.cursor.execute('SELECT reaction FROM matches WHERE user_id = '+str(user_id)+' AND match_user_id = '+str(matched_id)+'').fetchall()[0][0])
        return k
    def deletematch(self,user_id,matched_id):
        with self.connection:
            self.cursor.execute('DELETE FROM matches WHERE user_id = "'+str(user_id) +'" AND match_user_id = "'+str(matched_id)+'"')
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
db_worker = SQLighter(config.database_name)
for i in range(db_worker.count_rows()):
    Ud_dict.update({db_worker.id_list_full()[i][0]:db_worker.show_info(db_worker.id_list_full()[i][0])})
    matches_dict.update({db_worker.id_list_full()[i][0]:[]})
    profiles_dict.update({db_worker.id_list_full()[i][0]:[]})
print(Ud_dict)
print(matches_dict)
bot = telebot.TeleBot(config.TOKEN)
WEBHOOK_HOST = '46.181.240.60'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/home/jager/Desktop/kak/telechatbot/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '/home/jager/Desktop/kak/telechatbot/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.TOKEN)
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)
@bot.message_handler(commands=["start"])
def chenit(message):
    db_worker = SQLighter(config.database_name)
    var = db_worker.check_row(message.chat.id)
    varr = db_worker.check_state(message.chat.id)
    print(varr)
    if message.chat.id in Ud_dict:
        bot.send_message(message.chat.id,'Неверный ответ')
    else :
        if var[0] == (1,) and varr == [(message.chat.id, 8)] or varr == [(message.chat.id, 9)] or varr == [
            (message.chat.id, 10)]:
            bot.send_message(message.chat.id, 'nu normalno slushay')
        else:
            bot.send_message(message.chat.id, 'Как тебя зовут?')
            db_worker.new_row(message.chat.id)
            db_worker.state_update(message.chat.id, 1)
            Ud_dict.update({message.chat.id: db_worker.show_info(message.chat.id)})
            print(db_worker.show_info(message.chat.id))
            print(Ud_dict)
@bot.message_handler(commands=["showmyid"])
def showid(message):
    bot.send_message(message.chat.id, message.from_user.username)
@bot.message_handler(content_types=["text"])
def send_text(message):# Название функции не играет никакой роли, в принципe
    #name block
    if message.chat.id in Ud_dict and Ud_dict[message.chat.id][0][8] == 1 :
        Ud_dict[message.chat.id][0][1] = message.text
        Ud_dict[message.chat.id][0][8] = 2
        bot.send_message(message.chat.id, 'Кто ты? (Парень/Девушка)',reply_markup=keyboard7)
    # gender block
    elif message.chat.id in Ud_dict and  Ud_dict[message.chat.id][0][8] == 2 :
         if message.text.lower() == 'парень':
            Ud_dict[message.chat.id][0][2] = 1
            Ud_dict[message.chat.id][0][8] = 3
            bot.send_message(message.chat.id, 'Сколько тебе лет?')
         elif message.text.lower() == 'девушка':
            Ud_dict[message.chat.id][0][2] = 0
            Ud_dict[message.chat.id][0][8] = 3
            bot.send_message(message.chat.id, 'Сколько тебе лет?')
         else :
            bot.send_message(message.chat.id,'Неверный ответ')
            #age block
    elif message.chat.id in Ud_dict and  Ud_dict[message.chat.id][0][8] == 3 :
        if message.text.isdigit() and int(message.text) > 10 and int(message.text) < 99:
            Ud_dict[message.chat.id][0][3] = message.text
            Ud_dict[message.chat.id][0][8] = 4
            bot.send_message(message.chat.id, 'В каком городе ты живешь?')
        else:
            bot.send_message(message.chat.id,'Неверный ответ')
            #city block
    elif message.chat.id in Ud_dict and Ud_dict[message.chat.id][0][8] == 4:
        if type(message.text) == str:
            Ud_dict[message.chat.id][0][4] = message.text
            Ud_dict[message.chat.id][0][8] = 5
            bot.send_message(message.chat.id,'Кто тебе интересен?(Парни, Девушки, Все равно)',reply_markup=keyboard8)
        else:
            bot.send_message(message.chat.id,'Неверный ответ')
    #lookingfor block
    elif message.chat.id in Ud_dict and  Ud_dict[message.chat.id][0][8] == 5 :
        if message.text.lower() == 'парни':
            Ud_dict[message.chat.id][0][5] = 1
            Ud_dict[message.chat.id][0][8] = 6
            bot.send_message(message.chat.id, 'Расскажи о себе')
        elif message.text.lower() == 'девушки':
            Ud_dict[message.chat.id][0][5] = 2
            Ud_dict[message.chat.id][0][8] = 6
            bot.send_message(message.chat.id, 'Расскажи о себе')
        elif message.text.lower() == 'все равно':
             Ud_dict[message.chat.id][0][5] = 3
             Ud_dict[message.chat.id][0][8] = 6
             bot.send_message(message.chat.id, 'Расскажи о себе')
        else:
            bot.send_message(message.chat.id,'Неверный ответ')
            #self description block
    elif message.chat.id in Ud_dict and  Ud_dict[message.chat.id][0][8] == 6 :
         Ud_dict[message.chat.id][0][6] = message.text
         Ud_dict[message.chat.id][0][8] = 7
         bot.send_message(message.chat.id, 'Пришли мне своё фото')
         print(Ud_dict)
    else:
        db_worker = SQLighter(config.database_name)
        first_check = db_worker.check_state(message.chat.id)
        idii_list = db_worker.id_list(message.chat.id)
        if first_check == [(message.chat.id, 8,)] and message.text == str(1) or (first_check == [(message.chat.id, 9,)] and message.text == str(4)) or (first_check == [(message.chat.id, 12,)] and message.text == str(1)):
            # first_check passed (profile exists and fully filled)
            if message.chat.id in profiles_dict and len(profiles_dict[message.chat.id]) > 0 :
                bot.send_photo(message.chat.id, db_worker.show_info(profiles_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(profiles_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(profiles_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(profiles_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(profiles_dict[message.chat.id][-1])[0][6], reply_markup=keyboard2)
                db_worker.state_update(message.chat.id, 10)
            else:
                db_worker = SQLighter(config.database_name)
                preferences_check = db_worker.preference_check(message.chat.id)
                if preferences_check == [(1,)]:
                    profiles_list = []
                    for i in range(len(idii_list)):
                        if db_worker.gender_check(idii_list[i - 1][0]) == [(1,)]:
                            profiles_list.append(idii_list[i - 1][0])
                        random.shuffle(profiles_list)
                    if len(profiles_list) == 0:
                        bot.send_message(message.chat.id,'Кончились анкеты :(')
                    else:
                        bot.send_photo(message.chat.id, db_worker.show_info(profiles_list[-1])[0][7],
                                             caption=db_worker.show_info(profiles_list[-1])[0][1] +
                                                    ', ' + str(db_worker.show_info(profiles_list[-1])[0][3]) + ', '
                                                    + db_worker.show_info(profiles_list[-1])[0][4] + '\n' +
                                                     db_worker.show_info(profiles_list[-1])[0][6],reply_markup=keyboard2)
                        profiles_dict.update({message.chat.id : profiles_list})
                        print(profiles_dict)
                        db_worker.state_update(message.chat.id,10)

                elif preferences_check == [(2,)]:
                    profiles_list = []
                    for i in range(len(db_worker.id_list(message.chat.id))):
                        if db_worker.gender_check(idii_list[i - 1][0]) == [(0,)]:
                            profiles_list.append(idii_list[i - 1][0])
                            random.shuffle(profiles_list)
                    if len(profiles_list) == 0:
                        bot.send_message(message.chat.id,'Кончились анкеты :(')
                    else:
                        bot.send_photo(message.chat.id, db_worker.show_info(profiles_list[-1])[0][7],
                                           caption=db_worker.show_info(profiles_list[-1])[0][1] +
                                                   ', ' + str(db_worker.show_info(profiles_list[-1])[0][3]) + ', '
                                                   + db_worker.show_info(profiles_list[-1])[0][4] + '\n' +
                                                   db_worker.show_info(profiles_list[-1])[0][6],reply_markup=keyboard2)
                        db_worker.state_update(message.chat.id, 10)
                        profiles_dict.update({message.chat.id : profiles_list})
                        print(profiles_dict)
                else:
                    profiles_list = []
                    for i in range(len(db_worker.id_list(message.chat.id))):
                        profiles_list.append(idii_list[i - 1][0])
                    random.shuffle(profiles_list)
                    if len(profiles_list) == 0:
                        bot.send_message(message.chat.id,'Кончились анкеты :(')
                    else:
                        bot.send_photo(message.chat.id, db_worker.show_info(profiles_list[-1])[0][7],
                                        caption=db_worker.show_info(profiles_list[-1])[0][1] +
                                                    ', ' + str(db_worker.show_info(profiles_list[-1])[0][3]) + ', '
                                                    + db_worker.show_info(profiles_list[-1])[0][4] + '\n' +
                                                    db_worker.show_info(profiles_list[-1])[0][6],reply_markup=keyboard2)
                        profiles_dict.update({message.chat.id : profiles_list})
                        print(profiles_dict)
                        db_worker.state_update(message.chat.id, 10)
        elif first_check == [(message.chat.id, 8)] and message.text == str(2):
            bot.send_message(message.chat.id, '1.Заполнить анкету заново\n2.Изменить описание\n3.Изменить фото анкеты\n4.Посмотреть анкеты',reply_markup=keyboard5)
            db_worker.state_update(message.chat.id, 9)
            print(Ud_dict)
        elif first_check == [(message.chat.id, 9)] and message.text == str(1):
            bot.send_message(message.chat.id, 'Как тебя зовут?')
            db_worker.state_update(message.chat.id, 1)
            Ud_dict.update({message.chat.id:db_worker.show_info(message.chat.id)})
            print(Ud_dict)
        elif first_check == [(message.chat.id, 9)] and message.text == str(2):
            bot.send_message(message.chat.id,'Расскажи о себе немного(1 чтобы вернуться)',reply_markup=keyboard9)
            db_worker.state_update(message.chat.id, 14)
        elif first_check == [(message.chat.id, 9)] and message.text == str(3):
            bot.send_message(message.chat.id,'Отправь новую фотографию профиля')
            db_worker.state_update(message.chat.id,7)
            Ud_dict.update({message.chat.id:db_worker.show_info(message.chat.id)})
        elif first_check == [(message.chat.id, 14)] and message.text != str(1):
            Ud_dict.update({message.chat.id:db_worker.show_info(message.chat.id)})
            Ud_dict[message.chat.id][0][6] = message.text
            db_worker.send_info(Ud_dict[message.chat.id][0])
            if len(matches_dict[message.chat.id]) > 0:
                if len(matches_dict[message.chat.id]) > 1:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой' + str(
                        len(matches_dict[message.chat.id]) - 1) + ' ещё:')
                else:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой')
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0 :
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6] + '\n' + 'Пользователь оставил тебе сообщение '+str(db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id)) +'',reply_markup=keyboard4)
                db_worker.state_update(message.chat.id,17)
            else:
                db_worker.state_update(message.chat.id, 9)
                bot.send_message(message.chat.id,'Твой профиль:',disable_notification = True)
                bot.send_photo(message.chat.id, Ud_dict[message.chat.id][0][7],
                               caption=str(Ud_dict[message.chat.id][0][1]) + ', ' + str(Ud_dict[message.chat.id][0][3]) + ', ' +
                                       str(Ud_dict[message.chat.id][0][4]) + '\n' + str(Ud_dict[message.chat.id][0][6]))
                bot.send_message(message.chat.id,'1.Заполнить анкету заново\n2.Изменить описание\n3.Изменить фото анкеты\n4.Посмотреть анкеты',reply_markup=keyboard5)
        elif first_check == [(message.chat.id, 14)] and message.text == str(1):
            if len(matches_dict[message.chat.id]) > 0:
                if len(matches_dict[message.chat.id]) > 1:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ' + str(
                        len(matches_dict[message.chat.id]) - 1) + ' ещё:')
                else:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0 :
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6] + '\n' + 'Пользователь оставил тебе сообщение: '+str(db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id)) +'',reply_markup=keyboard4)
                db_worker.state_update(message.chat.id,17)
            else:
                db_worker.state_update(message.chat.id, 9)
                bot.send_message(message.chat.id,'Твой профиль:',disable_notification = True)
                bot.send_photo(message.chat.id, Ud_dict[message.chat.id][0][7],
                               caption=str(Ud_dict[message.chat.id][0][1]) + ', ' + str(Ud_dict[message.chat.id][0][3]) + ', ' +
                                       str(Ud_dict[message.chat.id][0][4]) + '\n' + str(Ud_dict[message.chat.id][0][6]))
                bot.send_message(message.chat.id,'1.Заполнить анкету заново\n2.Изменить описание\n3.Изменить фото анкеты\n4.Посмотреть анкеты',reply_markup=keyboard5)
        elif first_check == [(message.chat.id, 10,)] and (message.text == str(1) or message.text == '👍') :
            if len(profiles_dict[message.chat.id]) > 0:
                db_worker.create_match(message.chat.id, profiles_dict[message.chat.id][-1])
                matches_dict[profiles_dict[message.chat.id][-1]].append(message.chat.id)
                print(db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8])
                if db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 9 or db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 12 or db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 8:
                    db_worker.state_update(profiles_dict[message.chat.id][-1], 16)
                    print(db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8])
                    bot.send_message(profiles_dict[message.chat.id][-1],'1.Посмотреть кому ты понравился(ась) \n 2.Я не хочу больше никого искать',reply_markup=keyboard10)
                elif db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 15:
                    pass
                else:
                    bot.send_message(profiles_dict[message.chat.id][-1], 'Кто-то заинтересовался тобой, заканчивай с вопросом выше чтобы посмотреть')
                profiles_dict[message.chat.id].pop()
            if len(matches_dict[message.chat.id]) > 0 :
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0 :
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6] + '\n' + 'Пользователь оставил тебе сообщение: '+str(db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id)) +'',reply_markup=keyboard4)
                db_worker.state_update(message.chat.id,17)
            else:
                if len(profiles_dict[message.chat.id]) == 0:
                    bot.send_message(message.chat.id, 'Кончились анкеты :(')
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(profiles_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(profiles_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(profiles_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(profiles_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(profiles_dict[message.chat.id][-1])[0][6])
        elif first_check == [(message.chat.id, 10,)] and (message.text == str(2) or message.text == '💬'):
            if len(profiles_dict[message.chat.id]) == 0:
                bot.send_message(message.chat.id, 'Кончились анкеты :(')
            else:
                db_worker.state_update(message.chat.id, 11)
                bot.send_message(message.chat.id, 'Отправь своё сообщение или нажми (1) чтобы вернуться обратно',reply_markup=keyboard9)
                db_worker.state_update(message.chat.id, 11)
        elif first_check == [(message.chat.id, 10,)] and (message.text == str(3) or message.text == '👎'):
            if len(profiles_dict[message.chat.id]) > 0 :
                profiles_dict[message.chat.id].pop()
            if len(matches_dict[message.chat.id]) > 0 :
                if len(matches_dict[message.chat.id]) > 1:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ' + str(
                        len(matches_dict[message.chat.id]) - 1) + ' ещё:')
                else:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                   caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                           ', ' + str(
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                           + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                   caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                           ', ' + str(
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                           + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][
                                               6] + '\n' + 'Пользователь оставил тебе сообщение: ' + str(db_worker.check_text(
                                       matches_dict[message.chat.id][-1], message.chat.id)) + '',reply_markup=keyboard4)
                db_worker.state_update(message.chat.id, 17)
            else:
                if len(profiles_dict[message.chat.id]) == 0:
                    bot.send_message(message.chat.id, 'Кончились анкеты :(')
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(profiles_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(profiles_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(profiles_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(profiles_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(profiles_dict[message.chat.id][-1])[0][6])
        elif first_check == [(message.chat.id, 10,)] and (message.text == str(4) or message.text == '💤'):
            if len(matches_dict[message.chat.id]) > 0 :
                if len(matches_dict[message.chat.id]) > 1:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ' + str(
                        len(matches_dict[message.chat.id]) - 1) + ' ещё:')
                else:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                   caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                           ', ' + str(
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                           + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                   caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                           ', ' + str(
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                           + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][
                                               6] + '\n' + 'Кто-то заинтересовался тобой ' + str(db_worker.check_text(
                                       matches_dict[message.chat.id][-1], message.chat.id)) + '',reply_markup=keyboard4)
                db_worker.state_update(message.chat.id, 17)
            else:
                bot.send_message(message.chat.id,'1.Смотреть анкеты\n2.Посмотреть/редактировать мою анкету\n3.Не хочу никого искать',reply_markup=keyboard1)
                db_worker.state_update(message.chat.id,12)
        elif first_check == [(message.chat.id, 11,)]:
            if message.text != str(1):
                db_worker.create_match_and_text(message.chat.id, profiles_dict[message.chat.id][-1],
                                                            message.text)
                matches_dict[profiles_dict[message.chat.id][-1]].append(message.chat.id)
                if db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 9 or \
                        db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 12 or \
                        db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 8:
                    db_worker.state_update(profiles_dict[message.chat.id][-1], 16)
                    print(db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8])
                    bot.send_message(profiles_dict[message.chat.id][-1], '1.Посмотреть кому ты понравился(ась)\n2.Я не хочу больше никого искать',reply_markup=keyboard10)
                elif db_worker.show_info(profiles_dict[message.chat.id][-1])[0][8] == 15:
                    pass
                else:
                    bot.send_message(profiles_dict[message.chat.id][-1],
                                     'Кто-то заинтересовался тобой, заканчивай с вопросом выше чтобы посмотреть')
                if len(profiles_dict[message.chat.id]) > 0:
                    profiles_dict[message.chat.id].pop()
                if len(matches_dict[message.chat.id]) > 0:
                    if len(matches_dict[message.chat.id]) > 1:
                        bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ' + str(
                            len(matches_dict[message.chat.id]) - 1) + ' ещё:')
                    else:
                        bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                    if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0:
                        bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                    else:
                        bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][
                                                   6] + '\n' + 'Пользователь оставил тебе сообщение: ' + str(db_worker.check_text(
                                           matches_dict[message.chat.id][-1], message.chat.id)) + '',reply_markup=keyboard4)
                    db_worker.state_update(message.chat.id, 17)
                else:
                    if len(profiles_dict[message.chat.id]) == 0:
                        db_worker.state_update(message.chat.id, 10)
                        bot.send_message(message.chat.id, 'Анкеты кончились :(',reply_markup=keyboard2)
                    else:
                        bot.send_photo(message.chat.id,
                                               db_worker.show_info(profiles_dict[message.chat.id][-1])[0][7],
                                               caption=db_worker.show_info(profiles_dict[message.chat.id][-1])[0][1] +
                                                       ', ' + str(
                                                   db_worker.show_info(profiles_dict[message.chat.id][-1])[0][3]) + ', '
                                                       + db_worker.show_info(profiles_dict[message.chat.id][-1])[0][
                                                           4] + '\n' +
                                                       db_worker.show_info(profiles_dict[message.chat.id][-1])[0][6],reply_markup= keyboard2)
                        db_worker.state_update(message.chat.id, 10)
            else:
                if len(matches_dict[message.chat.id]) > 0:
                    if len(matches_dict[message.chat.id]) > 1:
                        bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ' + str(
                            len(matches_dict[message.chat.id]) - 1) + ' ещё:')
                    else:
                        bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                    if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0:
                        bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                    else:
                        bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][
                                                   6] + '\n' + 'Пользователь оставил тебе сообщение: ' + str(db_worker.check_text(
                                           matches_dict[message.chat.id][-1], message.chat.id)) + '',reply_markup=keyboard4)
                    db_worker.state_update(message.chat.id, 17)
                else:
                    db_worker.state_update(message.chat.id, 10)
                    bot.send_photo(message.chat.id,
                                       db_worker.show_info(profiles_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(profiles_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(profiles_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(profiles_dict[message.chat.id][-1])[0][
                                                   4] + '\n' +
                                               db_worker.show_info(profiles_dict[message.chat.id][-1])[0][6],reply_markup=keyboard2)
        elif first_check == [(message.chat.id, 12,)] and message.text == str(2):
            bot.send_photo(message.chat.id, db_worker.show_info(message.chat.id)[0][7],
                           caption=db_worker.show_info(message.chat.id)[0][1] +
                                   ', ' + str(
                               db_worker.show_info(message.chat.id)[0][3]) + ', '
                                   + db_worker.show_info(message.chat.id)[0][4] + '\n' +
                                   db_worker.show_info(message.chat.id)[0][6], )
            bot.send_message(message.chat.id, '1.Заполнить анкету заново\n2.Изменить описание\n3.Изменить фото анкеты\n4.Посмотреть анкеты',reply_markup=keyboard5)
            db_worker.state_update(message.chat.id, 9)
        elif first_check == [(message.chat.id, 12,)] and message.text == str(3):
            bot.send_message(message.chat.id,'Я буду скучать по тебе',reply_markup=keyboard6)
            db_worker.state_update(message.chat.id, 15)
        elif first_check ==[(message.chat.id,15,)] :
            if message.text == str(1) or message.text == '👍' :
                bot.send_message(message.chat.id,'Рад тебя видеть!')
                db_worker.state_update(message.chat.id, 12)
                bot.send_message(message.chat.id, '1.Смотреть анкеты\n2.Посмотреть/редактировать мою анкету\n3.Не хочу никого искать',reply_markup=keyboard1)
            else:
                bot.send_message(message.chat.id,'Нажми 1 для продолжения')
        elif first_check == [(message.chat.id,16)]  and (message.text == str(1) or message.text == '👍'):
            if len(matches_dict[message.chat.id]) > 1:
                bot.send_message(message.chat.id,
                                 'Кто-то заинтересовался тобой ' + str(len(matches_dict[message.chat.id]) - 1) + ' ещё:')
            else:
                bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
            if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0:
                bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                               caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                       ', ' + str(
                                   db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                       + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
            else:
                bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                               caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                       ', ' + str(
                                   db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                       + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][
                                           6] + '\n' + 'Пользователь оставил тебе сообщение: ' + str(db_worker.check_text(
                                   matches_dict[message.chat.id][-1], message.chat.id)) + '',reply_markup=keyboard4)
            db_worker.state_update(message.chat.id, 17)
        elif first_check == [(message.chat.id,16)] and (message.text == str(2) or message.text == '💤'):
            bot.send_message(message.chat.id, '1.Показать '+str(len(matches_dict[message.chat.id]))+' человек(a) которому(ым) ты понравился(ась)\n2.Я не хочу больше никого искать',reply_markup=keyboard4)
            db_worker.state_update(message.chat.id, 18)
        elif first_check == [(message.chat.id, 17,)] and (message.text == str(1) or message.text == '👍'):
            if len(matches_dict[message.chat.id]) > 0:
                bot.send_message(message.chat.id, 'Отлично,добавляй в друзья > @'+db_worker.show_info(matches_dict[message.chat.id][-1])[0][9]+'')
                bot.send_message(matches_dict[message.chat.id][-1],'Ты тоже понравился(ась) @'+db_worker.show_info(message.chat.id)[0][9]+'')
                bot.send_photo(matches_dict[message.chat.id][-1], db_worker.show_info(message.chat.id)[0][7],
                               caption=db_worker.show_info(message.chat.id)[0][1] + ', ' + str(
                                   db_worker.show_info(message.chat.id)[0][3]) + ', ' +
                                   db_worker.show_info(message.chat.id)[0][4] + '\n' +
                                   db_worker.show_info(message.chat.id)[0][6])
                db_worker.deletematch(matches_dict[message.chat.id][-1], message.chat.id)
                matches_dict[message.chat.id].pop()
            if len(matches_dict[message.chat.id]) == 0:
                db_worker.state_update(message.chat.id, 12)
                bot.send_message(message.chat.id, '1.Смотреть анкеты\n2.Посмотреть/редактировать мою анкету\n3.Не хочу никого искать',reply_markup=keyboard1)
            else:
                if len(matches_dict[message.chat.id]) > 1:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой '+str(len(matches_dict[message.chat.id])-1)+'человек ещё:')
                else:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0 :
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6] + '\n' + 'Пользователь оставил тебе сообщение: '+str(db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id)) +'',reply_markup=keyboard4)
        elif first_check == [(message.chat.id, 17,)] and (message.text == str(2) or message.text == '👎'):
            if len(matches_dict[message.chat.id]) > 0:
                db_worker.deletematch(matches_dict[message.chat.id][-1],message.chat.id)
                matches_dict[message.chat.id].pop()
            if len(matches_dict[message.chat.id]) == 0:
                db_worker.state_update(message.chat.id, 12)
                bot.send_message(message.chat.id,  '1.Смотреть анкеты\n2.Посмотреть/редактировать мою анкету\n3.Не хочу никого искать', reply_markup=keyboard1)
            else:
                if len(matches_dict[message.chat.id]) > 1:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой '+str(len(matches_dict[message.chat.id])-1)+' ещё:')
                else:
                    bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
                if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0 :
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
                else:
                    bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                                       caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                               ', ' + str(
                                           db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                               + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                               db_worker.show_info(matches_dict[message.chat.id][-1])[0][6] + '\n' + 'Пользователь оставил тебе сообщение: '+str(db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id)) +'',reply_markup=keyboard4)
        elif first_check == [(message.chat.id, 17,)] and (message.text == str(3) or message.text =='💤'):
            bot.send_message(message.chat.id, '1.Показать '+str(len(matches_dict[message.chat.id]))+' человек(a) которому(ым) ты понравился(ась)\n2.Я не хочу больше никого искать',reply_markup=keyboard4)
            db_worker.state_update(message.chat.id, 18)
        elif first_check == [(message.chat.id, 18,)] and (message.text == str(1) or message.text == '👍'):
            if len(matches_dict[message.chat.id]) > 1:
                bot.send_message(message.chat.id,
                                 'Кто-то заинтересовался тобой ' + str(len(matches_dict[message.chat.id]) - 1) + ' ещё:')
            else:
                bot.send_message(message.chat.id, 'Кто-то заинтересовался тобой ')
            if db_worker.check_text(matches_dict[message.chat.id][-1], message.chat.id) == 0:
                bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                               caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                       ', ' + str(
                                   db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                       + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][6],reply_markup=keyboard4)
            else:
                bot.send_photo(message.chat.id, db_worker.show_info(matches_dict[message.chat.id][-1])[0][7],
                               caption=db_worker.show_info(matches_dict[message.chat.id][-1])[0][1] +
                                       ', ' + str(
                                   db_worker.show_info(matches_dict[message.chat.id][-1])[0][3]) + ', '
                                       + db_worker.show_info(matches_dict[message.chat.id][-1])[0][4] + '\n' +
                                       db_worker.show_info(matches_dict[message.chat.id][-1])[0][
                                           6] + '\n' + 'Пользователь оставил тебе сообщение: ' + str(db_worker.check_text(
                                   matches_dict[message.chat.id][-1], message.chat.id)) + '',reply_markup=keyboard4)
            db_worker.state_update(message.chat.id, 17)
        elif first_check == [(message.chat.id, 18,)] and (message.text == str(2) or message.text == '💤'):
            bot.send_message(message.chat.id, 'Я буду скучать по тебе....',reply_markup= keyboard6)
            db_worker.state_update(message.chat.id, 15)
        else:
            bot.send_message(message.chat.id,'Неверный ответ')

@bot.message_handler(content_types="photo")
def profilepic(message):
        db_worker = SQLighter(config.database_name)
        if message.chat.id in Ud_dict and  Ud_dict[message.chat.id][0][8] == 7 :
            Ud_dict[message.chat.id][0][7] = message.photo[0].file_id
            Ud_dict[message.chat.id][0][8] = 8
            Ud_dict[message.chat.id][0][9] = message.from_user.username
            db_worker.send_info(Ud_dict[message.chat.id][0])
            bot.send_message(message.chat.id,'Твой профиль:',disable_notification = True)
            bot.send_photo(message.chat.id, Ud_dict[message.chat.id][0][7],
                               caption=str(Ud_dict[message.chat.id][0][1]) + ', ' + str(Ud_dict[message.chat.id][0][3]) + ', ' +
                                       str(Ud_dict[message.chat.id][0][4]) + '\n' + str(Ud_dict[message.chat.id][0][6]))
            bot.send_message(message.chat.id,'Все верно?\n1.Да\n2.Меню редактирования анкеты',reply_markup= keyboard3)
            if message.chat.id in matches_dict:
                pass
            else:
                matches_dict.update({message.chat.id:[]})
        else:
            bot.send_message(message.chat.id,'Неверный ответ')


            bot.send_message(Channel_Name, 'New rofl')
keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard5 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard6 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard7 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard8 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard9 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard10 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
keyboard1.row('1','2','3')
keyboard2.row('👍','💬','👎','💤')
keyboard3.row('1','2')
keyboard4.row('👍','👎','💤')
keyboard5.row('1','2','3','4')
keyboard6.row('👍')
keyboard7.row('Парень', 'Девушка')
keyboard8.row('Парни','Девушки','Все равно')
keyboard9.row('1')
keyboard10.row('👍','💤')
bot.remove_webhook()

 # Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})