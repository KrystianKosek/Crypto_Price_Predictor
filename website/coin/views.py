from django.http import HttpResponse
from django.template import loader
from utilities import update_data
from .models import CoinForTable


def index(request, coin_name):
    template = loader.get_template('coin_details.html')
    coin_id = CoinForTable.objects.get(name=coin_name).coin_id
    update_data.update_coin(coin_id)
    context = {}
    return HttpResponse(template.render(context, request))



