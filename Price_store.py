from threading import Lock
import json

class Price_store:
    
    def __init__(self):
        self.symbols = {
             "btcusdt":"BTC/USD",
            "ethusdt":"ETH/USD",
            "maticusdt":"MATIC/USD",
            "BTC/USD":"BTC/USD",
            "ETH/USD":"ETH/USD",
            "MATIC/USD":"MATIC/USD",
            "market.btcusdt.trade.detail":"BTC/USD",
            "market.maticusdt.trade.detail":"ETH/USD",
            "market.ethusdt.trade.detail":"MATIC/USD"
        }
        self.store = { i:{} for i in ["BTC/USD","ETH/USD","MATIC/USD"]}
        self.lock = Lock()
        self.len = 1
        
    def add(self,time,price,market):
        self.lock.acquire()
        if time in self.store[self.symbols[market]]:
            self.store[self.symbols[market]][time].append(price)
        else:
            self.store[self.symbols[market]][time] = [price]
            self.len+=1
        self.lock.release()
        
    def __str__(self):
        return json.dumps(self.store)
    def __len__(self):
        return self.len
    