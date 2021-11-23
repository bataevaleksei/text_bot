from logging import exception
import telebot
import config
import os
 
from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)
 
@bot.message_handler(commands=['start'])
def welcome(message):
 
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новый текст")
    item2 = types.KeyboardButton("Удалить")
    item3 = types.KeyboardButton("Найти")
 
    markup.add(item1, item2, item3)
 
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы сохранять сообщения.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.chat.type == 'private':

        # switch message.text
        if message.text == 'Новый текст':
            msg = bot.reply_to(message, 'Введите заголовок тeкста, который хотите добавить в систему')
            bot.register_next_step_handler(msg, new_head)
        elif message.text == 'Удалить':
            msg = bot.reply_to(message, 'Введите заголовок текста, который хотите удалить из системы')
            bot.register_next_step_handler(msg, delete_message)
        elif message.text == 'Найти':
            msg = bot.reply_to(message, 'Введите заголовок тeкста, который хотите найти')
            bot.register_next_step_handler(msg, find_message)
        else:
            bot.reply_to(message, 'Я тебя не понимаю 😭')

# get file_name
def new_head(message):
    try:
        file_name = message.text + "_" + str(message.chat.id) + ".txt"
        msg=bot.reply_to(message, 'Введите текст сообщения')
        bot.register_next_step_handler(msg, new_message, file_name)
    except Exception:
        bot.reply_to(message, 'Не получилось сохранить сообщение: ' + message.text)

# add message to the file
def new_message(message, file_name):
    try:
        open(file_name, 'w').write(message.text)
        bot.reply_to(message,'Данный текст успешно добавлен')
    except Exception:
        bot.reply_to(message,'Не получилось создать текст с заголовком: ' + message.text)

def delete_message(message):
    try:
        file_name = message.text + "_" + str(message.chat.id) + ".txt"
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
        os.remove(path)
        bot.send_message(message.chat.id, "Текст с заголовком " + message.text + " успешно удалён!")
    except Exception:
        bot.reply_to(message,"Не получилось удалить текст с заголовком: " + message.text + "\nВозможно такого заголовка не существует в системе")
        
def find_message(message):
    try:
        file_name= message.text + "_" + str(message.chat.id) + ".txt"
        bot.send_message(message.chat.id, open(file_name, 'r').read())
    except exception:
        bot.send_message(message.chat.id, "Не удалось найти текст по заголовку: " + message.text +"\nВозможно такого заголовка не существует в системе")

# RUN
bot.polling(none_stop=True)
