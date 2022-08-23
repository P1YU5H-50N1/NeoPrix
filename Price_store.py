from threading import Lock
import json
from datetime import datetime


class Price_store:

    def __init__(self):
        self.symbols = {
            "BTCUSDT": "BTC/USD",
            "ETHUSDT": "ETH/USD",
            "MATICUSDT": "MATIC/USD",
            "BTC/USD": "BTC/USD",
            "ETH/USD": "ETH/USD",
            "MATIC/USD": "MATIC/USD",
            "market.btcusdt.trade.detail": "BTC/USD",
            "market.maticusdt.trade.detail": "ETH/USD",
            "market.ethusdt.trade.detail": "MATIC/USD"
        }
        self.store = {i: {} for i in ["BTC/USD", "ETH/USD", "MATIC/USD"]}       
        self.lock = Lock()
        self.len = 1

    def __getitem__(self, market):
        while self.lock.locked():
            continue
        with self.lock:
            return self.store[market]

    def add(self, time, price, market, client):
        with self.lock:
            if client == 'FTX':
                time = int(datetime.strptime(
                    time, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp())
            elif client == 'HUOBI' or client == 'BINANCE':
                time = int(time/1000)

            if client == 'BINANCE':
                price = float(price)
            # print(f"{client}   {int(datetime.now().timestamp())}  CURRENT")
            print(
                f"{client}   {time}   {self.symbols[market]}  {price} {type(price)}")
            if time in self.store[self.symbols[market]]:
                last_avg_price, num_prices = self.store[self.symbols[market]][time]
                new_avg_price = ((last_avg_price*num_prices) +
                                price)/(num_prices+1)
                self.store[self.symbols[market]][time] = (
                    new_avg_price, num_prices+1)
            else:
                self.store[self.symbols[market]][time] = (price, 1)
                self.len += 1
            # print(
            #     f"{client} {time} {self.symbols[market]}  {self.store[self.symbols[market]][time]}")

    def __str__(self):
        return json.dumps(self.store)

    def __len__(self):
        return self.len
