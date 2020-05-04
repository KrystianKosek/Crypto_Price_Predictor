from random import shuffle
from coin.models import CoinForTable


def get_random_id() -> tuple:
    """
    Generate two random coin_id from coins existing in database
    Parameters:
        None
    Returns
        tuple: coin_id1, coin_id2
    """
    all_coins = CoinForTable.objects.values_list('coin_id', flat=True).distinct()
    all_coins = list(all_coins)
    shuffle(all_coins)
    return all_coins.pop(), all_coins.pop()
