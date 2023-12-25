import json
import requests

from elements import *

class ConvertException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertException('Ты конвертируешь валюту в ту же валюту? А ты хорош. Но играй по моим правилам')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'При обработке валюты {quote} что-то пошло не так (её нет)')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'При обработке валюты {base} что-то пошло не так (её нет)')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество в {amount}')

        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(
            f"https://api.fastforex.io/convert?from={keys[quote]}&to={keys[base]}&amount={amount}&api_key=8185d426ac-c104917bf6-s688he")
        result = json.loads(r.content)
        final_result = result["result"]

        return final_result
