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
