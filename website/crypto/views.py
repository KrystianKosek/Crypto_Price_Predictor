from django.http import HttpResponse
from django.template import loader
from utilities import make_plots


def index(request):
    make_plots.last_month("btc-bitcoin")
    make_plots.last_month("miota-iota")

    template = loader.get_template('home.html')
    context = {"img1_name": "Last month Bitcoin pricing", "img2_name": "Last month IOTA pricing"}
    return HttpResponse(template.render(context, request))