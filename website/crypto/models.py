from django.db import models
import datetime


class Currency(models.Model):
    currency_name = models.CharField(max_length=10, default='default')
    rate = models.FloatField(default=1.0)
    date = models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, 0))

    def __str__(self):
        return self.currency_name

    @staticmethod
    def delete_currencies():
        Currency.objects.all().delete()

