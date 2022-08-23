from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from BinanceClient import initializeBinance
from FTXClient import initializeFTX
from HuobiClient import initializeHuobi
from Price_store import Price_store
from Aggregator import Aggregator
import rel
import time
import signal as sys_signal
from threading import Event


def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def print_price(prices, evt):
    while True:
        if evt.is_set():
            return
        print(prices)
    # clear_line(len(prices))


evt = Event()
agg = Aggregator(evt)
prices = agg.get_price_store()


def handl():
    evt.set()
    rel.abort()
    print('Exit')


with ThreadPoolExecutor() as executor:
    f1 = executor.submit(initializeBinance, rel, prices)
    f2 = executor.submit(initializeFTX, rel, prices)
    f3 = executor.submit(initializeHuobi, rel, prices)
    f5 = executor.submit(agg.calculateAverage)
    # f4 = executor.submit(print_price,prices,evt)
    # print(f5.result())
    rel.signal(2, handl)  # Keyboard Interrupt
    rel.dispatch()
