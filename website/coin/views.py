from django.http import HttpResponse
from django.template import loader
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

    context.update({"coin_id": coin_name, "labels": labels, "data": data})

    return HttpResponse(template.render(context, request))



