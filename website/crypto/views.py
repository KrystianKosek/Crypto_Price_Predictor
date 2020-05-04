from django.http import HttpResponse
from django.template import loader
from utilities import make_plots, get_random_id, update_data
from coin.models import Coin, CoinForTable
from crypto.models import Currency


def index(request):
    coin1_id, coin2_id = get_random_id.get_random_id()

    update_data.update_coin(coin1_id)
    update_data.update_coin(coin2_id)
    path1 = make_plots.last_month(coin1_id, 'crypto')
    path2 = make_plots.last_month(coin2_id, 'crypto')

    template = loader.get_template('home.html')
    context = {"img1_name": f"Last month {coin1_id} pricing", "img2_name": f"Last month {coin2_id} pricing",
               "plot_path1": path1, "plot_path2": path2}

    all_coins = CoinForTable.objects.all()
    pln_course = Currency.objects.filter(currency_name="PLN")[0]
    pct_color_mapping = []
    i = 1
    for coin in all_coins:
        pct_color_mapping.append({"id": coin.rank, "name": coin.name, "price_USD": coin.price,
                                  "price_PLN": coin.price * pln_course.rate,
                                  "percent_change_24h": coin.percent_change_24h,
                                  "percent_change_7d": coin.percent_change_7d,
                                  "percent_change_30d": coin.percent_change_30d})
        if coin.percent_change_24h < 0:
            pct_color_mapping[i - 1].update({"24h_color": "red"})
        elif coin.percent_change_24h > 0:
            pct_color_mapping[i - 1].update({"24h_color": "green"})
        else:
            pct_color_mapping[i - 1].update({"24h_color": "black"})

        if coin.percent_change_7d < 0:
            pct_color_mapping[i - 1].update({"7d_color": "red"})
        elif coin.percent_change_7d > 0:
            pct_color_mapping[i - 1].update({"7d_color": "green"})
        else:
            pct_color_mapping[i - 1].update({"7d_color": "black"})

        if coin.percent_change_30d < 0:
            pct_color_mapping[i - 1].update({"30d_color": "red"})
        elif coin.percent_change_30d > 0:
            pct_color_mapping[i - 1].update({"30d_color": "green"})
        else:
            pct_color_mapping[i - 1].update({"30d_color": "black"})

        i += 1

    context.update({"table": pct_color_mapping})
    return HttpResponse(template.render(context, request))
