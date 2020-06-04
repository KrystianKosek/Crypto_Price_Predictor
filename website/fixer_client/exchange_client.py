import requests
import datetime
from crypto.models import Currency
from django.conf import settings


class ExchangeClient():
    def __init__(self):
        self.url = "http://data.fixer.io/api/latest"
        self.rate = 1.0

    def get_exchange_rate(self, currency_name: str) -> dict:
        Currency.delete_currencies()
        if currency_name == "USD":
            pass
        else:
            parameters = {"access_key": settings.FIXER_PASSWORD, "symbols": (currency_name + ",USD")}
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
        return rate_dict

    def process(self, currency: str = "PLN") -> None:
        self.get_exchange_rate(currency)

    def convert_currency(self, value: float) -> float:
        return value * self.rate

    def save_to_database(self, data: dict) -> None:
        new_currency_rate = Currency()
        new_currency_rate.currency_name = data["name"]
        new_currency_rate.rate = data["rate"]
        new_currency_rate.date = datetime.date.today()

        new_currency_rate.save()


if __name__ == "__main__":
    exchange = Exchange_client()
    exchange.process()
