import requests
import json
from bot_config import API_url


class APIException(Exception):
    pass

class ValuesException(Exception):
    pass


class APIRequest:

    def __init__(self):
        pass

    @staticmethod
    def get_prices(base, quote, amount):
        price = requests.get(API_url)
        if base == "RUB":
            base_ = 1
            quote_ = json.loads(price.content)["Valute"][quote]["Value"]

        elif quote == "RUB":
            base_ = json.loads(price.content)["Valute"][base]["Value"]
            quote_ = 1

        else:
            base_ = json.loads(price.content)["Valute"][base]["Value"]
            quote_ = json.loads(price.content)["Valute"][quote]["Value"]

        result = (base_ * amount) / quote_
        return result
