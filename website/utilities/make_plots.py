import glob

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from paprika_client.client import *


def last_month(coin_id: str) -> str:
    """
    Fetch data of specified coin_id from last month (if not fetched)
    Create visualisations of those data and save to coin_id_last_month.png in crypto/static/img dir
    Return path to a created plot
    """
    now = datetime.datetime.now()
    month_ealier = datetime.datetime(year=now.year, month=now.month - 1, day=now.day)
    filenames = glob.glob("data/*.json")
    needle = "{}_from_{}_to_{}.json".format(coin_id, month_ealier.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))
    needle = '/'.join(('data', needle))
    if needle not in filenames:
        client = Client()
        client.interval = "1h"

        client.coin_history(coin_id, month_ealier.strftime("%Y-%m-%d"))
        tickers = pd.read_json(needle)
        plt.style.use("seaborn-whitegrid")
        plt.figure(figsize=(16, 8))
        sns.lineplot(tickers['timestamp'], tickers['price'])
        plt.ylabel("Price [USD]")
        plt.xlabel("Date")
        plt.savefig("crypto/static/img/{}_last_month.png".format(coin_id))

    return "static/img/{}_last_month.png".format(coin_id)
