import datetime

from crypto.models import Coin
from paprika_client.client import *
from utilities._exceptions import FilterError


def update_coin(coin_id: str) -> None:
    """
    Fetch data of specified coin_id since the last fetch time.
    If there is no data of specified coin, fetch data from last month.
    Parameters:
        coin_id - string
    Returns:
        None
    """
    try:
        last_data = Coin.objects.filter(coin_id=coin_id).order_by('-datetime_stamp')[0].datetime_stamp
    except (IndexError, TypeError):
        now = datetime.datetime.now()
        last_data = datetime.datetime(year=now.year, month=now.month - 1, day=now.day)

    if last_data.date() != (datetime.datetime.now() + datetime.timedelta(days=-1)).date():
        client = Client()
        client.coin_history(coin_id, (last_data + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

