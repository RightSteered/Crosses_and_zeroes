import telebot
from bot_config import token
from extensions import *

bot = telebot.TeleBot(token)
keys = {
    "фунт": "GBP",
    "евро": "EUR",
    "доллар": "USD",
    "рубль": "RUB"
}


@bot.message_handler(commands=["start", "help"])
def start(message):
    man = "Для начала конвертации введите данные в следующем порядке:\n" \
          "1. Валюта, которую нужно сконвертировать\n2. Валюта, в которую нужно сконвертировать\n" \
          "3. Сумма конвертации (по умолчанию 1)\n" \
          "разделите вводимые данные пробелом.\n\nСписок доступных валют: /values\n" "Начать конвертацию: /convert"

    bot.reply_to(message, man)


@bot.message_handler(commands=["values"])
def show_values(message):
    text = "Доступные валюты:\n "
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=["convert"])
def start_convert(message):
    spec = "Введите валюту обмена, целевую валюту и сумму через пробел"
    bot.reply_to(message, spec)

    @bot.message_handler(content_types=["bot_command, text"])
    def convert(message: telebot.types.Message):
        values = list(message.text.lower().split(" "))
        if len(values) > 3:
            bot.reply_to(message, ValuesException("Ошибка! Проверьте заданные параметры!"))
            raise ValuesException("Ошибка! Проверьте заданные параметры!")

        elif len(values) == 2:
            amount = 1
            values.append(amount)
        base, quote, amount = values

        try:
            for i in keys.keys():
                if base == i:
                    base = keys[i]
                elif quote == i:
                    quote = keys[i]

        except APIException("Неизвестная валюта") as e:
            bot.reply_to(message, APIException)
            e = convert()
        finally:
            result = APIRequest.get_prices(base, quote, amount)
            return values, result

    print(convert(message))
    bot.reply_to(message, f"{convert(message)}")


bot.polling(none_stop=True)
