import requests
import json
from Config import currs


class ConversionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_prise(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException("Невозможно конвертировать одинаковые валюты")

        try:
            quote_ticker = currs[quote.lower()]
        except KeyError:
            raise ConversionException(f"Валюту {quote} невозможно конвертировать\nСписок доступных валют /values")

        try:
            base_ticker = currs[base.lower()]
        except KeyError:
            raise ConversionException(f"Валюту {base} невозможно конвертировать\nСписок доступных валют /values")

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConversionException("Не указано количество валюты для конвертации")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=\
{base_ticker}&from={quote_ticker}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "c4Rn3ETvjPfXQ3Bl9zLGDpDet3PcjKWL"
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        total = json.loads(response.text)
        total_res = total["result"]

        return round(total_res, 2)
