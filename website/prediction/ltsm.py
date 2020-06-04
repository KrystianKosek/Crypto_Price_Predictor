import json
import requests
import numpy as np
from coin.models import Coin
from utilities.update_data import update_coin
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, LSTM

CHUNK_SIZE = 5
N_SAMPLES = 720


class NNModel(object):
    def __init__(self, input_size=(720, 1), output_size=1, neurons=100,
                 activ_func='linear', dropout=0.2, loss='mse', optimizer='adam'):
        self.neurons = neurons
        self.activ_func = activ_func
        self.loss = loss
        self.model = Sequential()
        self.model.add(LSTM(neurons, input_shape=(5, 1)))
        self.model.add(Dropout(dropout))
        self.model.add(Dense(units=output_size))
        self.model.add(Activation(activ_func))
        self.model.compile(loss=loss, optimizer=optimizer)

    def fit(self, coin_id: str):
        X, y = self.preprocess(coin_id)
        history = self.model.fit(X.reshape(-1, 1), y, epochs=20, batch_size=5, verbose=1, shuffle=True)

    def preprocess(self, coin_id: str) -> np.array:
        latest_data = Coin.objects.filter(coin_id=coin_id).order_by("coin_id").distinct()[:N_SAMPLES]
        if len(latest_data) != N_SAMPLES:
            update_coin(coin_id)

        prices = np.array([item['price'] for item in latest_data.values("price")])
        prices = (prices - prices.std()) / prices.mean()
        prices = np.array_split(prices, N_SAMPLES / CHUNK_SIZE)
        return np.arange(1, 720), prices



