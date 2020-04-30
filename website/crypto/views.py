from django.http import HttpResponse
from django.template import loader
from utilities import make_plots, get_random_id, update_data
from paprika_client.client import *


def index(request):
    coin1_id = 'btc-bitcoin'
    coin2_id = 'miota-iota'
   # update_data.update_coin(coin1_id)
   # update_data.update_coin(coin2_id)

    path1 = make_plots.last_month(coin1_id)
    path2 = make_plots.last_month(coin2_id)

    template = loader.get_template('home.html')
    context = {"img1_name": f"Last month {coin1_id} pricing", "img2_name": f"Last month {coin2_id} pricing",
               "plot_path1": path1, "plot_path2": path2}

    return HttpResponse(template.render(context, request))
