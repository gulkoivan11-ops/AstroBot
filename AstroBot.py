import telebot
import os

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

def nice_format(num):
    if num.is_integer():
        return int(num)
    else:
        return round(num, 2)

values = {'секунд': 1, 'секунды': 1, 'сек': 1,'минут': 60, 'минуты': 60, 'мин': 60,'часов': 3600, 'часы': 3600, 'час': 3600}
def convert_units(value, time, secvalue):
    global values
    if secvalue in values:
        seconds = value * time * values[secvalue]
        resultsec = seconds
        resultmin = seconds / 60
        resulthour = seconds / 3600
        return resultsec, resultmin, resulthour
    else:
        return None
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я — бот, который может считать общее время экспозиции\nВведи, что ты хочешь конвертировать в таком виде:\n"5 кадров по 30 секунд"')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    try:
        parts = text.split(" по ")
        v = text.split(" кадров")
        value = float(v[0])
        time_and_2value = parts[1].split()
        time = int(time_and_2value[0])
        secvalue = time_and_2value[1]
        resultsec, resultmin, resulthour = convert_units(value, time, secvalue)
        if resultsec is not None and resultmin is not None and resulthour is not None:
            bot.send_message(message.chat.id,f"{nice_format(value)} кадров по {nice_format(time)} {(secvalue)} равняется:\n{nice_format(resultsec)} секунд\n{nice_format(resultmin)} минут\n{nice_format(resulthour)} часов")
        else:
            bot.send_message(message.chat.id,"Я не могу выполнить эту конвертацию. Попробуй еще раз")
    except Exception as e:
        print(f"Помилка: {e}")
        bot.send_message(message.chat.id,'Ошибка. Убедись, что введен правильный формат (например: "5 кадров по 30 секунд" / "10 кадров по 3 минуты"')

bot.infinity_polling()

