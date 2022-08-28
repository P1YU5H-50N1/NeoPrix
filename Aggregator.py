from Price_store import Price_store
from OHLC_store import OHLC_store
from datetime import datetime, timedelta
import json
import time


class Aggregator:
    def __init__(self, event):
        self.prices = Price_store()
        self.ohlc = OHLC_store()
        self.stop_event = event
        self.symbols = ["BTC", "ETH", "MATIC"]
        self.delta_1_min = 60
        self.delta_5_min = 60 * 5
        self.threshold = self.delta_1_min
        self.candle_start_1_min = int(datetime.now().timestamp())
        self.candle_end_1_min = self.candle_start_1_min + self.delta_1_min
        self.candle_start_5_min = int(datetime.now().timestamp())
        self.candle_end_5_min = self.candle_start_5_min + self.delta_5_min

    def get_price_store(self):
        """
        Returns the central price store
        for observers
        """
        return self.prices

    def get_candles(self, prices, delta, market):
        """
        Returns an OHLC object
        Args:
            prices: copy of prices for a symbol
            delta : time delta be it 1 min or 5 min
            market : symbol of instrument
        """
        count = 0
        price_high = -float("inf")
        price_low = float("inf")
        start = (
            self.candle_start_1_min
            if delta <= self.threshold
            else self.candle_start_5_min
        )
        end = (
            self.candle_end_1_min if delta <= self.threshold else self.candle_end_5_min
        )
        for i in sorted(prices.keys()):
            if i >= start and i < end:
                curr_price, _ = prices[i]
                price_open = curr_price if count == 0 else price_open
                price_low = min(price_low, curr_price)
                price_high = max(price_high, curr_price)
                price_close = curr_price
                count += 1
            elif i < self.candle_start_5_min:
                self.prices.pop(market, i)
            else:
                continue
        ohlc = {
            "timestamp": start,
            "time_start": datetime.fromtimestamp(start).strftime("%H:%M:%S"),
            "time_end": datetime.fromtimestamp(end).strftime("%H:%M:%S"),
            "type": "1-min" if delta <= self.threshold else "5-min",
            "open": price_open,
            "high": price_high,
            "low": price_low,
            "close": price_close,
        }
        return ohlc

    def candles_1_min(self):
        """
        Wrapper function for 1 min candles
        """
        for sym in self.symbols:
            print("AGGREGATOR", sym)
            latest = self.prices[sym]

            ohlc = self.get_candles(latest, self.delta_1_min, sym)
            ohlc["asset"] = sym
            # print(ohlc)
            self.ohlc.add(ohlc)
            self.ohlc.print_data()
        self.candle_start_1_min = self.candle_end_1_min
        self.candle_end_1_min += self.delta_1_min

    def candles_5_min(self):
        """
        Wrapper function for 5 min candles
        """
        for sym in self.symbols:
            print("AGGREGATOR", sym)
            latest = self.prices[sym]

            ohlc = self.get_candles(latest, self.delta_5_min, sym)
            ohlc["asset"] = sym
            self.ohlc.add(ohlc)
            self.ohlc.print_data()
        self.candle_start_5_min = self.candle_end_5_min
        self.candle_end_5_min += self.delta_5_min

    def calculate(self):
        """
        Main function which runs infinitely and generate candles
        """
        try:
            while True:
                if self.stop_event.is_set():
                    return
                if int(datetime.now().timestamp()) >= self.candle_end_1_min:
                    self.candles_1_min()
                elif int(datetime.now().timestamp()) >= self.candle_end_5_min:
                    self.candles_5_min()

                else:
                     self.stop_event.wait(
                        max(self.candle_end_1_min - int(datetime.now().timestamp()), 0)
                    )

        except Exception as e:
            print("AGGREGATOR ERR", e)
