import telebot
from bot_config import keys, token
from extensions import *

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", "help"])
def start(message):
    man = "Для начала конвертации введите данные в следующем порядке в любом регистре:\n" \
          "1. Валюта, которую нужно сконвертировать\n2. Валюта, в которую нужно сконвертировать\n" \
          "3. Сумма конвертации (по умолчанию 1)\n" \
          "разделите вводимые данные пробелом.\n \nСписок доступных валют: /values\n" "Начать конвертацию: /convert"

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

    @bot.message_handler(content_types=["text"])
    def convert(message: telebot.types.Message):
        values = list(message.text.lower().split(" "))

        while len(values) > 3:
            values.pop(-1)
        if len(values) == 2:  # Установка значения по умолчанию
            amount = "1"
            values.append(amount)

        if len(values) < 2:
            bot.reply_to(message, "Задано недостаточно параметров!")
            raise ValuesException("Задано недостаточно параметров!")

        base, quote, amount = values

        if base == quote:
            bot.reply_to(message, f"Нельзя конвертировать {base} в {quote}!")
            raise ValuesException()

        if not amount.isdigit() or int(amount) <= 0:
            bot.reply_to(message, f"Указана неверная сумма: {amount}!\n"
                                  f"Установлено значение по умолчанию.")
            amount = 1

        if base not in keys.keys():
            bot.reply_to(message, f"Неизвестная валюта {base}!")
            raise ApiException("Неизвестная валюта!")
        if quote not in keys.keys():
            bot.reply_to(message, f"Неизвестная валюта {quote}!")
            raise ApiException("Неизвестная валюта!")

        for i in keys.keys():
            if base == i:
                base = keys[i]
            elif quote == i:
                quote = keys[i]

        base_, base_nominal, quote_, quote_nominal = APIRequest.get_prices(base, quote)

        base_ = base_ / base_nominal
        quote_ = quote_ / quote_nominal

        result = round((base_ * int(amount) / quote_), 2)
        bot.reply_to(message, f"Стоимость {amount} {base} составляет {result} {quote}.")


bot.polling(none_stop=True)
