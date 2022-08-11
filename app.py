import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет,{message.chat.username}! Я умею конвертировать валюту. Чтобы узнать подробности нажми: /help")


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'чтобы узнать курс валют, следуйте примеру (всё пишем через пробел):\n<укажите валюту, которую нужно перевести, например, "доллар"> \
<напишите валюту, в которую вы хотите перевести первую валюту, например, "рубль"> \
<количество переводимой валюты>\nВ итоге запрос должен выглядеть так: доллар рубль 1\nМожно выбрать и другие валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Вы ввели слишком много параметров!')


        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    text = f'цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)