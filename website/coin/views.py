from crypto.models import Currency
from django.http import HttpResponse
from django.template import loader
from prediction.sarimax import predict as prediction
from utilities import update_data

from .models import CoinForTable, Coin


def index(request, coin_name):
    template = loader.get_template('coin_details.html')
    coin = CoinForTable.objects.get(name=coin_name)
    update_data.update_coin(coin.coin_id)
    context = {}

    query_set = Coin.objects.filter(coin_id=coin.coin_id)
    labels = []
    data = []
    for x in query_set:
        labels.append(str(x.datetime_stamp.date()))
        data.append(str(x.price))

    pln_course = Currency.objects.filter(currency_name="PLN")[0]
    context.update({"coin_id": coin.coin_id, "coin_name": coin_name, "labels": labels, "data": data})
    context.update({"price_USD": coin.price, "price_PLN": coin.price * pln_course.rate,
                    "percent_change_24h": coin.percent_change_24h, "percent_change_7d": coin.percent_change_7d,
                    "percent_change_30d": coin.percent_change_30d, "beta_value": coin.beta_value,
                    "circulating_supply": coin.circulating_supply, "volume_24h": coin.volume_24h,
                    "change_24h": coin.change_24h, "market_cap": coin.market_cap,
                    "coin_ranking": int(coin.coin_ranking), "coin_name": coin.name})

    if coin.max_supply == 0.0:
        context.update({"max_supply": "undefined"})
    else:
        context.update({"max_supply": coin.max_supply})

    cases = {coin.percent_change_24h: "24h_color",
             coin.percent_change_7d: "7d_color",
             coin.percent_change_30d: "30d_color",
             coin.change_24h: "change_color"}

    for case in cases:
        if case < 0:
            context.update({cases[case]: "red"})
        elif case > 0:
            context.update({cases[case]: "green"})
        else:
            context.update({cases[case]: "black"})

    return HttpResponse(template.render(context, request))


def predict(request, coin_name):
    template = loader.get_template('predict.html')
    df = prediction(CoinForTable.objects.get(name=coin_name).coin_id)

    labels = []

    for i in df.index.values:
        labels.append(str(i)[11: 16])

    context = {}
    context.update({"prediction_index": labels,
                    "lower_pred_price": df['lower price'].values,
                    "upper_pred_price": df['upper price'].values
                    })
    return HttpResponse(template.render(context, request))
