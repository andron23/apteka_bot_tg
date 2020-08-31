import telebot 
#import dbworker
#import config4 as config
import requests
from telebot import types
import requests
import json
from datetime import datetime
from bonus_api import Bonus

API_Token = "1213910596:AAGTixK8EYXSrFgTLlvdtk62LeUw1NFUxgk"
bot = telebot.TeleBot(API_Token)
ids = {}
states_db = {}
#print(states_db)
states = {
    'check_balance': 1, 
    'enter_card': 2, 
    'enter_birthdate': 3, 
    'enter_phone': 4, 
    'enter_name': 5
}

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%d.%m.%Y")
    d2 = datetime.strptime(d2, "%d.%m.%Y")
    return (d2 - d1).days

@bot.message_handler(commands=['start'])
def greeting(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    balance_but = types.InlineKeyboardButton(text="Баланс", callback_data="balance_check")
    register_but = types.InlineKeyboardButton(text="Регистрация", callback_data="register")
    keyboard.add(balance_but)
    keyboard.add(register_but)
    bot.reply_to(message, "Привет! Если хочешь проверить свой баланс, набери /balance.", reply_markup = keyboard)

@bot.message_handler(commands=['balance'])
def balance(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Введите номер телефона.")
    states_db[chat_id] = states['check_balance']
    #dbworker.set_state(chat_id, config.States.S_ENTER_PHONE.value)

@bot.message_handler(func=lambda message: states_db[message.chat.id] == states['check_balance'])
def user_entering_phone(message):
    phone = message.text
    con = Bonus()
    balance = con.check_balance(phone = phone)
    #card_info = requests.get('https://bonus.rarus-online.com:88/organization/card?phone={}'.format(phone), headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token})
    #balance = card_info.json()['cards'][0]['actual_balance']
    bot.reply_to(message, "Баланс Вашей карты: {} бонусов.".format(balance))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "balance_check":
            chat_id=call.message.chat.id
            bot.send_message(chat_id, text="Введите номер телефона.")
            states_db[chat_id] = states['check_balance']
            #dbworker.set_state(chat_id, config.States.S_ENTER_PHONE.value)
        elif call.data == "register":
            chat_id=call.message.chat.id
            bot.send_message(chat_id, text="Отлично, для начала, введите номер своей карты.")
            states_db[chat_id] = states['enter_card']
            #dbworker.set_state(chat_id, config.States.S_ENTER_CARD.value) 
        elif call.data == "male":
            chat_id=call.message.chat.id 
            id = ids[chat_id]
            con = Bonus()
            con.update_user_info(id = id, key = 'gender', value = 'male')
            #requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                  #headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                  #json = {'gender': 'male'})
            bot.send_message(chat_id, text="Введите Вашу дату рождения. Например: 01.01.1900")
            states_db[chat_id] = states['enter_birthdate']
            #dbworker.set_state(chat_id, config.States.S_ENTER_DATE.value)
        elif call.data == "female":
            chat_id=call.message.chat.id 
            id = ids[chat_id]
            con = Bonus()
            con.update_user_info(id = id, key = 'gender', value = 'female')
            #requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                  #headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                  #json = {'gender': 'female'})
            bot.send_message(chat_id, text="Введите Вашу дату рождения. Например: 01.01.1900")
            states_db[chat_id] = states['enter_birthdate']
            #dbworker.set_state(chat_id, config.States.S_ENTER_DATE.value)
            #keyboard = types.InlineKeyboardMarkup()
            #balance_but = types.InlineKeyboardButton(text="Баланс", callback_data="balance_check") 
            #keyboard.add(balance_but)   
            #bot.send_message(chat_id, text="Вы успешно зарегистрированы! Хотите узнать свой баланс?", reply_markup = keyboard)
        elif call.data == "accept":
            chat_id=call.message.chat.id 
            id = ids[chat_id]
            con = Bonus()
            con.update_user_info(id = id, key = 'recieve_notifications', value = 1)
            #res = requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                 # headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                  #json = {'recieve_notifications': 1})
            #print(res.json())
            keyboard = types.InlineKeyboardMarkup()
            balance_but = types.InlineKeyboardButton(text="Баланс", callback_data="balance_check") 
            keyboard.add(balance_but)   
            bot.send_message(chat_id, text="Вы успешно зарегистрированы! Хотите узнать свой баланс?", reply_markup = keyboard)
        elif call.data == "not_accept":
            chat_id=call.message.chat.id 
            id = ids[chat_id]
            con = Bonus()
            con.update_user_info(id = id, key = 'recieve_notifications', value = 0)            
            #requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                  #headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                  #json = {'recieve_notifications': 0})
            keyboard = types.InlineKeyboardMarkup()
            balance_but = types.InlineKeyboardButton(text="Баланс", callback_data="balance_check") 
            keyboard.add(balance_but)   
            bot.send_message(chat_id, text="Вы успешно зарегистрированы! Хотите узнать свой баланс?", reply_markup = keyboard)


@bot.message_handler(func=lambda message: states_db[message.chat.id] == states['enter_card'])
def user_entering_barcode(message):
    global ids
    chat_id = message.chat.id
    card = message.text
    con = Bonus()
    id = con.get_user_id(card = card)
    #card_info = requests.get('https://bonus.rarus-online.com:88/organization/card?barcode={}'.format(card), headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token})
    #id = card_info.json()['cards'][0]['user_id']
    ids[chat_id] = id
    bot.send_message(chat_id, text="Введите Ваш телефон.")
    states_db[chat_id] = states['enter_phone']
    #dbworker.set_state(chat_id, config.States.S_ENTER_PHONE_REG.value)

@bot.message_handler(func=lambda message: states_db[message.chat.id] == states['enter_phone'])
def user_entering_phone_reg(message):
    global ids
    chat_id = message.chat.id
    phone = message.text
    id = ids[chat_id]
    con = Bonus()
    con.update_user_info(id = id, key = 'phone', value = '{}'.format(phone))    
    #requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                  #headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                  #json = {'phone': '{}'.format(phone)})
    bot.send_message(chat_id, text="Введите Ваше имя, фамилию и отчество.")
    states_db[chat_id] = states['enter_name']
    #dbworker.set_state(chat_id, config.States.S_ENTER_NAME.value)
    #print("Name ok")

@bot.message_handler(func=lambda message: states_db[message.chat.id] == states['enter_name'])
def user_entering_name(message):
    global ids
    chat_id = message.chat.id
    name = message.text
    id = ids[chat_id]
    con = Bonus()
    con.update_user_info(id = id, key = 'name', value = '{}'.format(name))
    #requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                 # headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                  #json = {'name': '{}'.format(name)})
    keyboard = types.InlineKeyboardMarkup()
    man_but = types.InlineKeyboardButton(text="Мужской", callback_data="male")
    woman_but = types.InlineKeyboardButton(text="Женский", callback_data="female")
    keyboard.add(man_but)
    keyboard.add(woman_but)
    bot.reply_to(message, "Выберите свой пол.", reply_markup = keyboard)
    
    

@bot.message_handler(func=lambda message: states_db[message.chat.id] == states['enter_birthdate'])
def user_entering_date(message):
    global ids
    chat_id = message.chat.id
    date = message.text
    date = days_between('01.01.1970',date)*24*60*60*1000
    id = ids[chat_id]
    con = Bonus()
    con.update_user_info(id = id, key = 'birthdate', value = date)   
    #requests.post('https://bonus.rarus-online.com:88/organization/user/{}'.format(id), 
                 # headers = {'Content-Type': 'application/json;charset:UTF-8', 'token':token}, 
                 # json = {'birthdate': date})
      
    #dbworker.set_state(chat_id, config.States.S_ACCEPT.value)
    keyboard = types.InlineKeyboardMarkup()
    accept_but = types.InlineKeyboardButton(text="Согласен", callback_data="accept")
    notaccept_but = types.InlineKeyboardButton(text="Не согласен", callback_data="not_accept")
    keyboard.add(accept_but)
    keyboard.add(notaccept_but)
    print("But ok")
    bot.reply_to(message, "Отлично, остался один шаг. Вы согласны иногда получать от нас полезные сообщения?", reply_markup = keyboard)


#@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ACCEPT.value)
#def user_accepting(message):
#    global ids
#    print("Start")
#    chat_id = message.chat.id
#    keyboard = types.InlineKeyboardMarkup()
#    accept_but = types.InlineKeyboardButton(text="Согласен", callback_data="accept")
#    notaccept_but = types.InlineKeyboardButton(text="Не согласен", callback_data="not_accept")
#    keyboard.add(accept_but)
#    keyboard.add(notaccept_but)
#    print("But ok")
#    bot.reply_to(message, "Отлично, остался один шаг. Вы согласны иногда получать от нас полезные сообщения?", reply_markup = keyboard)


if __name__ == '__main__': 
    bot.polling(none_stop = True)       