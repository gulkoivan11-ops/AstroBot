import telebot
import os
from flask import Flask, request

token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(token)

def nice_format(num):
    if num.is_integer():
        return int(num)
    else:
        return round(num, 2)

values = {
    'секунд': 1, 'секунды': 1, 'сек': 1,
    'минут': 60, 'минуты': 60, 'мин': 60,
    'часов': 3600, 'часы': 3600, 'часа': 3600, 'час': 3600
}

def convert_units(value, time, secvalue):
    if secvalue in values:
        seconds = value * time * values[secvalue]
        return seconds, seconds / 60, seconds / 3600
    return None, None, None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я — бот, который может считать общее время экспозиции\n'
        'Введи, что ты хочешь конвертировать в таком виде:\n'
        '"5 кадров по 30 секунд"'
    )

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

        if resultsec is not None:
            bot.send_message(
                message.chat.id,
                f"{nice_format(value)} кадров по {nice_format(time)} {secvalue} равняется:\n"
                f"{nice_format(resultsec)} секунд\n"
                f"{nice_format(resultmin)} минут\n"
                f"{nice_format(resulthour)} часов"
            )
        else:
            bot.send_message(message.chat.id, "Я не могу выполнить эту конвертацию. Попробуй ещё раз")
    except Exception:
        bot.send_message(
            message.chat.id,
            'Ошибка. Убедись, что введен правильный формат '
            '(например: "5 кадров по 30 секунд" / "10 кадров по 3 минуты")'
        )

app = Flask(__name__)

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def health():
    return "ok"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.environ["RENDER_EXTERNAL_URL"] + "/telegram")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
