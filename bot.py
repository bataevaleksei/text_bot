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
    item3 = types.KeyboardButton("Просмотреть")
    item4 = types.KeyboardButton("Показать все заголовки")
 
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы сохранять сообщения.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

    try:
        if not os.path.isdir(str(message.chat.id)):
            os.mkdir(str(message.chat.id))
    except Exception:
        bot.send_message(message.chat.id,"Cant sigh up")

@bot.message_handler(content_types=['text'])
def main(message):
    if message.chat.type == 'private':
        try:
            os.chdir(str(message.chat.id))
        except Exception:
            bot.reply_to(message, 'directory fail')
            welcome(message)

        # switch message.text
        if message.text == 'Новый текст':
            msg = bot.reply_to(message, 'Введите заголовок тeкста, который хотите добавить в систему')
            bot.register_next_step_handler(msg, new_head)
        elif message.text == 'Удалить':
            msg = bot.reply_to(message, 'Введите заголовок текста, который хотите удалить из системы')
            bot.register_next_step_handler(msg, delete_message)
        elif message.text == 'Просмотреть':
            msg = bot.reply_to(message, 'Введите заголовок тeкста, который хотите просмотреть')
            bot.register_next_step_handler(msg, find_message)
        elif message.text == 'Показать все заголовки':
           show_all(message)
        else:
            bot.reply_to(message, 'Я тебя не понимаю 😭')
        os.chdir("..")


# get file_name
def new_head(message):
    try:
        os.chdir(str(message.chat.id))
        print(os.getcwd())
        file_name = message.text + ".txt"
        msg = bot.reply_to(message, 'Введите текст сообщения')
        bot.register_next_step_handler(msg, new_message, file_name)
    except Exception:
        bot.reply_to(message, 'Не получилось сохранить сообщение: ' + message.text)


# add message to the file
def new_message(message, file_name):
    try:
        open(file_name, 'w').write(message.text)
        bot.reply_to(message, 'Данный текст успешно добавлен')
    except Exception:
        bot.reply_to(message, 'Не получилось создать текст с заголовком: ' + message.text)
    os.chdir("..")


def delete_message(message):
    try:
        os.chdir(str(message.chat.id))
        file_name = message.text + ".txt"
        os.remove(file_name)
        bot.send_message(message.chat.id, "Текст с заголовком " + message.text + " успешно удалён!")
        os.chdir("..")
    except Exception:
        bot.reply_to(message, "Не получилось удалить текст с заголовком: " + message.text + "\nВозможно такого заголовка не существует в системе")



def find_message(message):
    try:
        os.chdir(str(message.chat.id))
        file_name = message.text + ".txt"
        bot.send_message(message.chat.id, open(file_name, 'r').read())
        os.chdir("..")
    except Exception:
        bot.send_message(message.chat.id, "Не удалось найти текст по заголовку: " + message.text + "\nВозможно такого заголовка не существует в системе")



def show_all(message):
    try:
        print("Все папки и файлы:", os.listdir())
        bot.send_message(chat_id=message.chat.id, text=str(os.listdir()))
    except Exception:
        bot.send_message(message.chat.id, "Не удалось отобразить список ваших текстов")

# RUN
bot.polling(none_stop=True)
