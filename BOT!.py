import telebot
from extensions import ConverterException, Convertor
from config import Token, exchanges
import traceback

bot = telebot.TeleBot(Token)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = {f"Привет!Нажми /values и введи валюту, потом валюту в которую перевести и сумму"}
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConverterException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except ConverterException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")

    else:
        bot.reply_to(message, answer)


bot.polling()
