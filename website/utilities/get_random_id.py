import glob
import random

import pandas as pd

from paprika_client.client import *


def get_random_id() -> str:
    """
    Fetch data of all today currencies if needed and return one randomly chosen coin_id
    """
    now = datetime.datetime.now()
    filenames = glob.glob("data/*.json")
    needle = "all_coins_{}.json".format(now.strftime("%Y-%m-%d"))
    needle = '/'.join(('data', needle))
    if needle not in filenames:
        client = Client()
        client.all_today_coins()

    tickers = pd.read_json(needle)
    return tickers['id'][random.randint(0, len(needle))]
