import requests
import argparse

import datetime
from ._validations import is_date_valid, code_error
from crypto.models import *


class Client(object):

    def __init__(self):
        self.interval = "1h"
        self.now = datetime.datetime.now()
        self.cur_datetime = datetime.datetime.now()
        self.base_url = "https://api.coinpaprika.com/v1/"
        self.parser = argparse.ArgumentParser(description="Process requests for paprikacoin API data")
        self.parser.add_argument('-t', '--today', action='store', dest='coin',
                           help="Get today data of specific coin - pass coin_id")
        self.parser.add_argument('-ch', '--history', action='store', nargs='+', dest='coin_history',
                           help="Get historical data of specific coin - pass [coin-id] [history start date] YYYY-MM-DD")
        self.parser.add_argument('-a', '--all', action='store_true', dest='fetch_all',
                            help='Get all current data')

    def process(self) -> None:
        args = self.parser.parse_args()
        if args.coin:
            self.today_coin(args.coin)
        elif args.coin_history:
            coin_id, start_date = args.coin_history
            print(coin_id, start_date)
            self.coin_history(coin_id, start_date)
        elif args.fetch_all:
            self.all_today_coins()

    def today_coin(self, coin_id: str) -> None:
        get_coin_url = "/".join((self.base_url, "tickers", coin_id))
        daily_coin = requests.get(url=get_coin_url)
        code_error(daily_coin.status_code)
        filename = "{}_{}.json".format(coin_id, self.cur_datetime.strftime("%Y-%m-%d"))
        self._save_json(daily_coin, filename)


    def all_today_coins(self) -> None:
        get_all_coins_url = "/".join((self.base_url, 'tickers'))
        all_daily_coins = requests.get(url=get_all_coins_url)
        code_error(all_daily_coins.status_code)
        Coin.delete_coins()
        CoinForTable.delete_coins()
        self._save_database(all_daily_coins.json(), "CoinForTable")
        self._save_database(all_daily_coins.json(), "all")


    def coin_history(self, coin_id: str, start_date: str) -> None:
        if is_date_valid(start_date):
            get_coin_history_url = "/".join((self.base_url, 'tickers', coin_id, 'historical'))
            coin_history = requests.get(url=get_coin_history_url, params={"start": start_date,
                                                                          "interval": self.interval})
            code_error(coin_history.status_code)
            self._save_database(coin_history.json(), coin_id)


    def _save_database(self, data: requests.request, id: str) -> None:
        if id == 'all':
            ctr = 0
            samples = len(data)
            for coin in data:
                month_ealier = datetime.datetime(year=self.now.year, month=self.now.month - 1, day=self.now.day)
                self.coin_history(coin['id'], month_ealier.strftime("%Y-%m-%d"))
                ctr += 1
                print("downloaded {} progress: {}/{}".format(coin['id'], ctr, samples))
        elif id == 'CoinForTable':
            for coin in data:
                new_coin = CoinForTable()
                new_coin.price = coin["quotes"]["USD"]["price"]
                new_coin.coin_id = coin["id"]
                new_coin.coin_name = coin["name"]
                new_coin.percent_change_24h = coin["quotes"]["USD"]['percent_change_24h']
                new_coin.percent_change_7d = coin["quotes"]["USD"]['percent_change_7d']
                new_coin.percent_change_30d = coin["quotes"]["USD"]['percent_change_30d']

                new_coin.datetime_stamp = coin['last_updated']
                new_coin.save()
        else:
            for coin in data:
                new_coin = Coin()
                new_coin.price = coin['price']
                new_coin.coin_id = id
                new_coin.datetime_stamp = coin['timestamp']
                new_coin.save()

if __name__ == '__main__':
    client = Client()
    client.process()



