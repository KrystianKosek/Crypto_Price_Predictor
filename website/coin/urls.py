from django.urls import path
from . import views


urlpatterns = [
    path('<str:coin_name>', views.index, name='index'),
    path('<str:coin_name>/predict', views.predict, name='predict'),
]