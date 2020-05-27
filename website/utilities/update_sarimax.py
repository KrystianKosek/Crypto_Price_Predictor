from prediction.sarimax import fit_parameters
from coin.models import CoinForTable


def update_hyperparams() -> None:
    all_cryptos = CoinForTable.objects.all()
    for crypto in all_cryptos:
        print("[*] Fitting sarimax hyperparams for {}".format(crypto.coin_id))
        fit_parameters(crypto.coin_id)
        print("[*] Fitting ended")