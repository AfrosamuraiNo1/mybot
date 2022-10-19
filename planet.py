import ephem
from datetime import datetime

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
