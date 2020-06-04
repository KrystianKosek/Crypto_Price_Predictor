import datetime
from coin.models import Coin
from crypto.models import Currency
from paprika_client.client import Client
from fixer_client.exchange_client import ExchangeClient


def update_coin_for_table() -> None:
    client = Client()
    client.all_today_coins()


def update_course(name: str) -> None:
    last_date = Currency.objects.filter(currency_name="PLN").first().date
    actual_date = datetime.datetime.today() - datetime.timedelta(days=1)
    if last_date.date() < actual_date.date():
        Currency.delete_currencies()
        cl = ExchangeClient()
        cl.get_exchange_rate(name)


def update_coin(coin_id: str) -> None:
    client = Client()
    now = datetime.datetime.now()

    try:
        last_data = Coin.objects.filter(coin_id=coin_id).order_by('-datetime_stamp')[0].datetime_stamp
        if last_data.day != now.day:
            client.coin_history(coin_id, last_data.strftime("%Y-%m-%d"))
            print("Fetching from {}".format(last_data.strftime("%Y-%m-%d")))
    except (IndexError, TypeError) as e:
        month_ealier = datetime.datetime(year=now.year, month=now.month - 1, day=now.day)
        print("Loading coin failed, fetching {} last month data".format(coin_id))
        client.coin_history(coin_id, month_ealier.strftime("%Y-%m-%d"))




