from threading import Lock
import json
from datetime import datetime
from copy import deepcopy


class Price_store:
    def __init__(self):
        self.symbols = {
            "BTCUSDT": "BTC",
            "ETHUSDT": "ETH",
            "MATICUSDT": "MATIC",
            "BTC/USD": "BTC",
            "ETH/USD": "ETH",
            "MATIC/USD": "MATIC",
            "market.btcusdt.trade.detail": "BTC",
            "market.maticusdt.trade.detail": "MATIC",
            "market.ethusdt.trade.detail": "ETH",
        }
        self.store = {i: {} for i in ["BTC", "ETH", "MATIC"]}
        self.lock = Lock()
        self.len = 1

    def pop(self, market, ts):
        """
        Deletes a particular timestamp from 
        price store for a crypto
        """
        with self.lock:
            del self.store[market][ts]

    def __getitem__(self, market):
        """
        Returns a deepcopy of current
        price store
        """
        with self.lock:
            t = deepcopy(self.store[market])
        return t

    def add(self, time, price, market, client):
        """
        Calculates the average price via previous
        average price and replaces it with new average
        for a particular time stamps and market
        """
        with self.lock:
            if client == "FTX":
                time = int(
                    datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
                )
            elif client == "HUOBI" or client == "BINANCE":
                time = int(time / 1000)

            if client == "BINANCE":
                price = float(price)
            if time in self.store[self.symbols[market]]:
                last_avg_price, num_prices = self.store[self.symbols[market]][time]
                new_avg_price = ((last_avg_price * num_prices) + price) / (
                    num_prices + 1
                )
                self.store[self.symbols[market]][time] = (new_avg_price, num_prices + 1)
            else:
                self.store[self.symbols[market]][time] = (price, 1)
                self.len += 1

    def __str__(self):
        """
        Returns JSON representation of price store
        """
        return json.dumps(self.store)

    def __len__(self):
        return self.len
