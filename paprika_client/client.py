import requests
import argparse
import os
import json
import datetime
from _validations import is_date_valid, code_error


class Client(object):
    """
    Client instance is used to fetch cryptocurrency data from coinpaprika.com
    It uses coinpaprika API
    It is possible to fetch three types of data ( because it meets my needs )
    1. Today's data of specific cryptocurrency
    2. Historical data of specifiv crypocurrency, from provided date
    3. Today's data of all cryptocurrencies
    """
    def __init__(self):
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
        """Process command line arguments and invoke appropirate methods"""
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
        """
        Fetch current data of specific cryptocurrency (coin_id)
        Save to file in format {coin_id}_{current_date}.json
        Parameters:
            coin_id: string-like id of specific coin
        Returns:
            None
        """
        get_coin_url = os.path.join(self.base_url, "tickers", coin_id)
        daily_coin = requests.get(url=get_coin_url)
        code_error(daily_coin.status_code)
        filename = "{}_{}.json".format(coin_id, self.cur_datetime.strftime("%Y-%m-%d"))
        self._save_json(daily_coin, filename)

    def coin_history(self, coin_id: str, start_date: str) -> None:
        """
        Fetch historical data of specific cryptocurrency (coin_id), from start_date
        Save to file {coin_id}_from_{start_date}_to_{current_date}.json
        Parameters:
            coin_id: string-like id of specific coin
            start_date: string-like date formated "YYYY-MM-DD"
        Returns:
            None
        """
        if is_date_valid(start_date):
            get_coin_history_url = os.path.join(self.base_url, 'tickers', coin_id, 'historical')
            coin_history = requests.get(url=get_coin_history_url, params={"start": start_date})
            code_error(coin_history.status_code)
            filename = "{}_from_{}_to_{}.json".format(coin_id, start_date, self.cur_datetime.strftime("%Y-%m-%d"))
            self._save_json(coin_history, filename)

    def all_today_coins(self) -> None:
        """
        Fetch current data of all cryptocurrencies
        Save to file all_coins_{current_date}.json
        Returns:
            None
        """
        get_all_coins_url = os.path.join(self.base_url, 'tickers')
        all_daily_coins = requests.get(url=get_all_coins_url)
        code_error(all_daily_coins.status_code)
        filename = "all_coins_{}.json".format(self.cur_datetime.strftime("%Y-%m-%d"))
        self._save_json(all_daily_coins, filename)


    @staticmethod
    def _save_json(data: requests.request, filename: str) -> None:
        """
        Save data to file named filename (json)
        Parameters:
            data: request.request - object that contains response from requests.get
            filename: str
        """
        with open(f"data/{filename}", 'w') as fp:
            json.dump(data.json(), fp)


if __name__ == '__main__':
    client = Client()
    client.process()



