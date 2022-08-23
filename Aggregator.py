from Price_store import Price_store
from datetime import datetime, timedelta
import time


class Aggregator:
    def __init__(self, event):
        self.prices = Price_store()
        self.stop_event = event
        self.symbols = ["BTC/USD", "ETH/USD", "MATIC/USD"]
        self.candle_start_1_min = int(datetime.now().timestamp())
        self.candle_end_1_min = self.candle_start_1_min + 15
        self.candle_start_5_min = int(datetime.now().timestamp())
        self.candle_end_5_min = self.candle_start_5_min + 60 * 5
        self.avg_prices_1_min = {i: [] for i in self.symbols}
        self.candles_1_min = []

    def get_price_store(self):
        return self.prices

    def calculateAverage(self):
        try:
            while True:
                if self.stop_event.is_set():
                    return

                for sym in self.symbols:
                    print("AGGREGATOR", sym)
                    time.sleep(1)
                    # t = self.prices[sym]
                    for i in self.prices[sym]:
                        print(
                            "AGGREGATOR ----------------------------- ",
                            i,
                            self.prices[sym][i][0],
                        )
        except Exception as e:
            print("AGGREGATOR", e)

            # print("      ",self.candle_end_1_min - int(datetime.now().timestamp()),end="\r")
            # if self.candle_end_1_min - int(datetime.now().timestamp()) == 0:
            #     print(self.candle_start_1_min)
            #     for sym in self.symbols:
            #         temp = self.prices[sym]
            #         print(temp)
            # for t in self.prices[sym]:
            # print(sym, t, self.prices[sym][t])

            # if datetime.now().timestamp() >= self.candle_end_1_min :
            #     start = self.candle_start_1_min
            #     for sym in self.symbols:
            #         high, low = 0, float('inf')
            #         print("AGGREGATOR",sym, self.prices[sym])
            #         for t in self.prices[sym].keys():
            #             if self.prices[sym][t] < self.candle_end_1_min:
            #                 p = self.prices[sym][t]
            #                 high = max(high,p)
            #                 low = min(low,p)
            #                 self.avg_prices_1_min[sym].append((t,self.prices[sym][t]))
            #         print(self.avg_prices_1_min)
            #         self.avg_prices_1_min[sym] = sorted(self.avg_prices_1_min[sym],key  = lambda x : x[0])
            #         open_candle = self.avg_prices_1_min[sym][0][1]
            #         close_candle = self.avg_prices_1_min[sym][-1][1]
            #         self.avg_prices_1_min[sym] = []
            #         print(sym, open_candle,close_candle,high,low, self.candle_start_1_min,self.candle_end_1_min)
            #     self.candle_start_1_min = self.candle_end_1_min
            #     self.candle_end_1_min = self.candle_start_1_min + 60
