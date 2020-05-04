import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from coin.models import Coin
from utilities._exceptions import FilterError


def clean_image_dir(curr_date: str, app_name: str) -> None:
    """
    Clean not up-to-date last_month/ plots
    Parameters:
        curr_date - string-like date, suggested YYYY-MM-DD
    Returns:
        None
    """
    dirname = f"{app_name}/static/img/last_month/"
    images = os.listdir(dirname)
    for image in images:
        if image.split('_')[-1] != curr_date.strftime("%Y-%m-%d") + ".png":
            os.remove(''.join([dirname, image]))


def last_month(coin_id: str, app_name: str) -> str:
    """
    Fetch data of specified coin_id from last month (if not fetched)
    Create visualisations of those data and save to coin_id_up_to_date.png in app_name/static/img dir
    Return path to a created plot
    Parameters:
        coin_id - string, id of coin to plot
    Returns:
        path-like string, path to plot image
    """
    now = datetime.datetime.now()
    month_ealier = datetime.datetime(year=now.year, month=now.month - 1, day=now.day)
    filename = "{}/static/img/last_month/{}_up_to_{}.png".format(app_name, coin_id, now.strftime("%Y-%m-%d"))
    if not os.path.exists(filename):
        last_month_coins = Coin.objects.filter(coin_id=coin_id, datetime_stamp__range=[month_ealier, now])
        if not last_month_coins:
            raise FilterError("Not found {} data from last month".format(coin_id))
        prices = last_month_coins.values_list('price', flat=True)
        datetime_stamps = last_month_coins.values_list('datetime_stamp', flat=True)

        plt.style.use("seaborn-whitegrid")
        plt.figure(figsize=(16, 8))
        sns.lineplot(datetime_stamps, prices)
        plt.ylabel("Price [USD]")
        plt.xlabel("Date")

        plt.savefig(filename.format(coin_id))

    clean_image_dir(now, app_name)
    return "/img/last_month/{}".format(os.path.basename(filename))
