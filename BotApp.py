import telebot
from Config import currs, TOKEN
from extensions import Converter, ConversionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def helper(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n<Валюта для конвертации> \
<В какую валюту конвертировать> <количество валюты для конвертации>\n Увидеть список всех доступных валют /values "
    bot.reply_to(message, text)


@bot.message_handler(commands=["values", ])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for k in currs.keys():
        text = "\n".join((text, k, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        m_values = message.text.split()

        if len(m_values) != 3:
            raise ConversionException("Неправильный запрос. Неправильное количество параметров")

        quote, base, amount = m_values
        total_res = Converter.get_prise(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"{amount} {quote} = {total_res} {base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
