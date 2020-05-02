from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/pln', views.index_pln, name ='pln-home'),
    # path('/coin/<str:coin_id>', views.show)
]