import itertools
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from coin.models import Coin
from django_pandas.io import read_frame
from pylab import rcParams

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')


def get_data_frame(coin_id: str, records=720) -> pd.DataFrame:
    """
    Generate a DataFrame containing price data of the selected cryptocurrency,
    which is indexed with a price record datetime.

    Parameters:
        coin_id: string - name of cryptocurrency
        records: int - number of records to be saved in the DataFrame
    Returns
        pd.DataFrame
    """
    try:
        qs = Coin.objects.filter(coin_id=coin_id).order_by('datetime_stamp')
        qs = qs[qs.count() - records:]
    except IndexError:
        qs = Coin.objects.filter(coin_id=coin_id).order_by('datetime_stamp')[:]

    index = pd.date_range(qs[0].datetime_stamp, periods=qs.count(), freq='1H', tz=None)
    df = read_frame(qs, index_col=index).drop(columns=['id', 'coin_id', 'datetime_stamp'])
    return df


def handle(df):
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(df.price, model='additive')
    fig = decomposition.plot()
    plt.show()

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

    mod = sm.tsa.statespace.SARIMAX(df,
                                    order=best_params[0],
                                    seasonal_order=best_params[1],
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    print('SARIMA{}x{}12 - AIC:{}'.format(best_params[0], best_params[1], best_aic))
    results = mod.fit()
    results.plot_diagnostics(figsize=(18, 8))
    plt.show()

    pred = results.get_prediction(start=int(df.size * 0.9), dynamic=False)
    pred_ci = pred.conf_int()
    ax = df.iloc[int(df.size * 0.5):].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='Ahead Forecast', alpha=.7, figsize=(14, 4))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Retail_sold')
    plt.legend()
    plt.show()

    pred_uc = results.get_forecast(steps=12)
    pred_ci = pred_uc.conf_int()
    ax = df.iloc[int(df.size * 0.9):].plot(label='observed', figsize=(14, 4))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    pass
