import itertools
import json
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from coin.models import Coin
from django_pandas.io import read_frame

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')


def get_data_frame(coin_id: str, records=720) -> pd.DataFrame:
    try:
        qs = Coin.objects.filter(coin_id=coin_id).order_by('datetime_stamp')
        qs = qs[qs.count() - records:]
    except IndexError:
        qs = Coin.objects.filter(coin_id=coin_id).order_by('datetime_stamp')[:]

    index = pd.date_range(qs[0].datetime_stamp, periods=qs.count(), freq='1H', tz=None)
    df = read_frame(qs, index_col=index).drop(columns=['id', 'coin_id', 'datetime_stamp'])
    return df


def fit_parameters(coin_id: str):
    df = get_data_frame(coin_id)
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 24) for x in list(itertools.product(p, d, q))]
    best_params = 0
    best_aic = 0
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(df, order=param, seasonal_order=param_seasonal,
                                                enforce_stationarity=False, enforce_invertibility=False)
                results = mod.fit()
                if best_aic == 0:
                    best_aic = results.aic
                    best_params = param, param_seasonal
                elif results.aic < best_aic:
                    best_aic = results.aic
                    best_params = param, param_seasonal
            except:
                continue

    dict_data = {coin_id: best_params}

    with open("hyperparams/{}.json".format(coin_id), "w+") as f:
        json.dump(dict_data, f)


def predict(coin_id):
    df = get_data_frame(coin_id)
    with open("hyperparams/{}.json".format(coin_id), "r") as f:
        param_dict = json.load(f)

    coin_best_params = param_dict[coin_id]
    mod = sm.tsa.statespace.SARIMAX(df,
                                    order=coin_best_params[0],
                                    seasonal_order=coin_best_params[1],
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    pred_uc = results.get_forecast(steps=12)
    pred_ci = pred_uc.conf_int()
    return pred_ci


if __name__ == "__main__":
    pass
