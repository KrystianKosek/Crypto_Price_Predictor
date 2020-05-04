from datetime import datetime
from coin.models import Coin
from paprika_client.client import Client


def update_coin(coin_id: str) -> None:
    """
    Fetch data of specified coin_id since the last fetch time.
    If there is no data of specified coin, fetch data from last month.
    Parameters:
        coin_id - string
    Returns:
        None
    """
    client = Client()
    now = datetime.now()

    try:
        last_data = Coin.objects.filter(coin_id=coin_id).order_by('-datetime_stamp')[0].datetime_stamp
        if last_data.day != now.day:
            client.coin_history(coin_id, last_data.strftime("%Y-%m-%d"))
            print("Fetching from {}".format(last_data.strftime("%Y-%m-%d")))
    except (IndexError, TypeError) as e:
        month_ealier = datetime(year=now.year, month=now.month - 1, day=now.day)
        print("Loading coin failed, fetching {} last month data".format(coin_id))
        client.coin_history(coin_id, month_ealier.strftime("%Y-%m-%d"))




