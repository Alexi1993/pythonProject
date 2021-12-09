import requests
import json
from config import exchanges


class ConverterException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ConverterException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ConverterException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise ConverterException(f'Нельзя переводить одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f'Введите другую сумму {amount}!')

        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message
