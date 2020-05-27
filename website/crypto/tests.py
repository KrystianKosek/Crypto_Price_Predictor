from django.test import TestCase
from crypto.models import Currency
from fixer_client.exchange_client import ExchangeClient


class CurrencyTestCase(TestCase):
    def setUp(self) -> None:
        self.cl = ExchangeClient()

    def test_currency_rate_in_database(self):
        Currency.delete_currencies()
        self.cl.get_exchange_rate("PLN")
        self.assertIsNotNone(Currency.objects.filter(currency_name="PLN")[0])
