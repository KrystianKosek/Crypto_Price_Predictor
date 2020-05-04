import requests
import json
import os
import datetime
from crypto.models import Currency


class ExchangeClient():
    # client made for getting currency rate from fixer api
    def __init__(self):
        self.url = "http://data.fixer.io/api/latest"
        self.password = "7d2b1c67a29c26c7bbeafe09ea4c0d0a"
        self.rate = 1.0

    # gets 1 dollar rate in chosen currency
    def get_exchange_rate(self, currency_name: str) -> dict:
        Currency.delete_currencies()
        if currency_name == "USD":
            pass
        else:
            parameters = {"access_key": self.password, "symbols": (currency_name + ",USD")}
            try:
                response = requests.get(self.url, params=parameters)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print("An error has occured: {err}")
            else:
                data = response.json()
                self.rate = data["rates"][currency_name] / data["rates"]["USD"]

        rate_dict = {"rate": self.rate, "name": currency_name}
        self.save_to_database(rate_dict)
        #self.save_to_json(rate_dict)
        return rate_dict

    # method processing get function for chosen currency
    # default currency is PLN
    def process(self,currency: str = "PLN") -> None:
        self.get_exchange_rate(currency)

    # converts value in dollars to other currency set in client
    def convert_currency(self,value: float) -> float:
        return value*self.rate

    def save_to_database(self,data: dict) -> None:
        new_currency_rate = Currency()
        new_currency_rate.currency_name = data["name"]
        new_currency_rate.rate = data["rate"]
        new_currency_rate.date = datetime.date.today()

        new_currency_rate.save()

    # saves current rate to json
    # example file look: {"rate": 4.0, "name": "PLN"}
    @staticmethod
    def save_to_json(data: dict) -> None:
        if not os.path.exists("data"):
            os.mkdir("data")
        with open("data/rate.json", 'w') as f:
            json.dump(data, f)


if __name__ == "__main__":
    exchange = ExchangeClient()
    exchange.process()
