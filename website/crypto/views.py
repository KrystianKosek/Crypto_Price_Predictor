from django.http import HttpResponse
from django.template import loader
from utilities import make_plots, get_random_id, update_data
from paprika_client.client import *
from crypto.models import *
import datetime


def index(request):
    coin1_id, coin2_id = get_random_id.get_random_id()

    update_data.update_coin(coin1_id)
    update_data.update_coin(coin2_id)
    path1 = make_plots.last_month(coin1_id)
    path2 = make_plots.last_month(coin2_id)

    template = loader.get_template('home.html')
    context = {"img1_name": f"Last month {coin1_id} pricing", "img2_name": f"Last month {coin2_id} pricing",
               "plot_path1": path1, "plot_path2": path2}

    all_cryptos = CoinForTable.objects.all()
    mapa = []
    i = 1
    for x in all_cryptos:
        mapa.append({"id":i, "name": x.coin_id, "price": x.price, "percent_change_24h": x.percent_change_24h, "percent_change_7d": x.percent_change_7d, "percent_change_30d": x.percent_change_30d})
        i += 1

    context.update({"table": mapa})
    return HttpResponse(template.render(context, request))
