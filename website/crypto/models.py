from django.db import models
import datetime


class Coin(models.Model):
    coin_id = models.CharField(max_length=30, default='default')
    datetime_stamp = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0))
    price = models.FloatField(default=0.0)

    def __str__(self):
        return "{} {}".format(self.coin_id, self.datetime_stamp)

    @staticmethod
    def delete_coins():
        Coin.objects.all().delete()

class CoinForTable(models.Model):
    coin_id = models.CharField(max_length=30, default='default')
    datetime_stamp = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0))
    price = models.FloatField(default=0.0)
    percent_change_24h = models.FloatField(default=0.0)
    percent_change_7d = models.FloatField(default=0.0)
    percent_change_30d = models.FloatField(default=0.0)

    def __str__(self):
        return "{} {}".format(self.coin_id, self.datetime_stamp)

    @staticmethod
    def delete_coins():
        CoinForTable.objects.all().delete()

class Currency(models.Model):
    currency_name = models.CharField(max_length=10, default='default')
    rate = models.FloatField(default=1.0)
    date = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0))

    def __str__(self):
        return self.currency_name

    @staticmethod
    def delete_currencies():
        Currency.objects.all().delete()