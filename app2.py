import telebot
from extensions import *
from elements import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}.\n"
                                      f"Спасибо, что ты меня запустил, а то я спать устал. \n"
                                      f"Если не знаете, как со мной работать, напишите /help")

@bot.message_handler(commands=['help'])
def send_some_help(message):
    bot.send_message(message.chat.id, f"Этот бот предназначен для конвертации обычных валют. \n"
                                      f"Список доступных валют можно просмотреть с помощью команды /values. \n"
                                      f"Для того, чтобы сконвертировать одну валюту в другую, нужно придерживаться следующего формата: \n"
                                      f"Валюта, которую вы конвертируете, валюта, в которую в конвертируете, количество \n"
                                      f"Успехов Вам!")

@bot.message_handler(commands=['values'])
def values_list(message: telebot.types.Message):
    text = 'Валюты, которые здесь доступны \n(Помните, что валюту надо вводить точь-в-точь): '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convertion(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Параметров должно быть ровно три')

        quote, base, amount = values

        final_result = CurrencyConverter.get_price(quote, base, amount)
    except ConvertException as n:
        bot.reply_to(message, f'Ошибка пользователя.\n{n}')
    except Exception as n:
        bot.reply_to(message, f'Не удалось обработать команду, а жаль.\n{n}')
    else:
        text = f"Цена {amount} {quote} в {base} = {final_result}"
        bot.reply_to(message, text)


bot.polling(none_stop=True)
