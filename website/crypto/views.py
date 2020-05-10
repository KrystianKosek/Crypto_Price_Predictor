from django.http import HttpResponse
from django.template import loader
from utilities import get_random_id, update_data
from paprika_client.client import *
from coin.models import Coin, CoinForTable
from crypto.models import Currency


def index(request):
    coin1_id, coin2_id = get_random_id.get_random_id()
    #update_data.update_coin(coin1_id)
    #update_data.update_coin(coin2_id)
    update_data.update_course("PLN")

    template = loader.get_template('home.html')

    context = {}

    all_cryptos = CoinForTable.objects.all()
    pln_course = Currency.objects.filter(currency_name = "PLN")[0]

    mapa = []
    i = 1
    for x in all_cryptos:
        mapa.append({"id": i, "name": x.name, "price_USD": x.price, "price_PLN": x.price * pln_course.rate,
                     "percent_change_24h": x.percent_change_24h, "percent_change_7d": x.percent_change_7d,
                     "percent_change_30d": x.percent_change_30d})
        if x.percent_change_24h < 0:
            mapa[i - 1].update({"24h_color": "red"})
        elif x.percent_change_24h > 0:
            mapa[i - 1].update({"24h_color": "green"})
        else:
            mapa[i - 1].update({"24h_color": "black"})

        if x.percent_change_7d < 0:
            mapa[i - 1].update({"7d_color": "red"})
        elif x.percent_change_7d > 0:
            mapa[i - 1].update({"7d_color": "green"})
        else:
            mapa[i - 1].update({"7d_color": "black"})

        if x.percent_change_30d < 0:
            mapa[i - 1].update({"30d_color": "red"})
        elif x.percent_change_30d > 0:
            mapa[i - 1].update({"30d_color": "green"})
        else:
            mapa[i - 1].update({"30d_color": "black"})

        i += 1

    query_set = Coin.objects.filter(coin_id=coin1_id)
    query_set2 = Coin.objects.filter(coin_id=coin2_id)

    labels = []
    labels2 = []
    data = []
    data2 = []
    name = all_cryptos.filter(coin_id = coin1_id).first().name
    name2 = all_cryptos.filter(coin_id = coin2_id).first().name

    for x in query_set:
        labels.append(str(x.datetime_stamp.date()))
        data.append(str(x.price))

    for x in query_set2:
        labels2.append(str(x.datetime_stamp.date()))
        data2.append(str(x.price))

    context.update({"coin1_id": name, "labels": labels, "data": data})
    context.update({"coin2_id": name2, "labels2": labels2, "data2": data2})

    context.update({"table": mapa})
    return HttpResponse(template.render(context, request))
