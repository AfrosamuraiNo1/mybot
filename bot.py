import logging
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from random import randint, choice
from glob import glob
from emoji import emojize

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!")

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
#    username = update.effective_user.first_name
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']


def planet_user(update, context):
    print('Вызван /planet')
    update.message.reply_text('Введи планету по англиский. Напимер Mars')

def planet(update, context):
    planet = update.message.text
    dt_now = datetime.now()
    time_now = dt_now.strftime('%Y/%m/%d')
    name_planet = getattr(ephem,planet[0:].capitalize())(time_now)
    constellation = ephem.constellation(name_planet)
    update.message.reply_text(f'В созвездии сегодня находится планета {constellation}')

def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message)

def send_foto_picture(update, context):
    foto_photos_list = glob('img/*.jp*g')
    foto_pic_filename = choice(foto_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(foto_pic_filename, 'rb'))


def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    # Командуем боту начать ходить в Telegram за сообщениями
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("cat", send_foto_picture))
    dp.add_handler(CommandHandler("planet", planet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(MessageHandler(Filters.text, planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

if __name__ == "__main__":
    main()