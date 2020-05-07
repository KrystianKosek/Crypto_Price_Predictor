import datetime

from crypto.models import Coin, Currency
from paprika_client.client import Client
from fixer_client.exchange_client import Exchange_client

def update_course(name: str) -> None:
    last_date = Currency.objects.filter(currency_name = "PLN").first().date
    actual_date = datetime.datetime.today() - datetime.timedelta(days=1)
    if last_date.date() < actual_date.date():
        Currency.delete_currencies()
        cl = Exchange_client()
        cl.get_exchange_rate(name)

def update_coin(coin_id: str) -> None:
    try:
        last_data = Coin.objects.filter(coin_id=coin_id).order_by('-datetime_stamp')[0].datetime_stamp
    except (IndexError, TypeError):
        now = datetime.datetime.now()
        last_data = datetime.datetime(year=now.year, month=now.month - 1, day=now.day)

    if last_data.date() != (datetime.datetime.now() + datetime.timedelta(days=-1)).date():
        client = Client()
        client.coin_history(coin_id, (last_data + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

