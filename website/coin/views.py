from django.http import HttpResponse
from django.template import loader
from utilities import update_data
from .models import CoinForTable, Coin
from crypto.models import Currency


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

    pln_course = Currency.objects.filter(currency_name = "PLN")[0]
    context.update({"coin_id": coin_name, "labels": labels, "data": data})
    context.update({"price_USD": coin.price, "price_PLN": coin.price * pln_course.rate, "percent_change_24h": coin.percent_change_24h, "percent_change_7d": coin.percent_change_7d,
                    "percent_change_30d": coin.percent_change_30d, "beta_value": coin.beta_value, "circulating_supply": coin.circulating_supply,
                    "volume_24h": coin.volume_24h, "change_24h": coin.change_24h,
                    "market_cap": coin.market_cap, "coin_ranking": int(coin.coin_ranking),"coin_name": coin.name})
    if coin.max_supply == 0.0:
        context.update({"max_supply": "undefined"})
    else:
        context.update({"max_supply": coin.max_supply})

    if coin.percent_change_24h < 0:
        context.update({"24h_color": "red"})
    elif coin.percent_change_24h > 0:
        context.update({"24h_color": "green"})
    else:
        context.update({"24h_color": "black"})

    if coin.percent_change_7d < 0:
        context.update({"7d_color": "red"})
    elif coin.percent_change_7d > 0:
        context.update({"7d_color": "green"})
    else:
        context.update({"7d_color": "black"})

    if coin.percent_change_30d < 0:
        context.update({"30d_color": "red"})
    elif coin.percent_change_30d > 0:
        context.update({"30d_color": "green"})
    else:
        context.update({"30d_color": "black"})

    if coin.change_24h < 0:
        context.update({"change_color": "red"})
    elif coin.change_24h > 0:
        context.update({"change_color": "green"})
    else:
        context.update({"change_color": "black"})

    return HttpResponse(template.render(context, request))


def predict(request, coin_name):
    return HttpResponse(coin_name)


