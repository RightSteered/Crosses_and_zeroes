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
    def get_prices(base, quote):
        price = requests.get(API_url)
        if base == "RUB":
            base_ = 1
            base_nominal = 1
            quote_ = json.loads(price.content)["Valute"][quote]["Value"]
            quote_nominal = json.loads(price.content)["Valute"][quote]["Nominal"]
            return base_, base_nominal, quote_, quote_nominal

        elif quote == "RUB":
            base_ = json.loads(price.content)["Valute"][base]["Value"]
            base_nominal = json.loads(price.content)["Valute"][base]["Nominal"]
            quote_ = 1
            quote_nominal = 1
            return base_, base_nominal, quote_, quote_nominal

        else:
            base_ = json.loads(price.content)["Valute"][base]["Value"]
            base_nominal = json.loads(price.content)["Valute"][base]["Nominal"]
            quote_ = json.loads(price.content)["Valute"][quote]["Value"]
            quote_nominal = json.loads(price.content)["Valute"][quote]["Nominal"]

            return base_, base_nominal, quote_, quote_nominal
