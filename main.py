from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from BinanceClient import initializeBinance
from FTXClient import initializeFTX
from HuobiClient import initializeHuobi
from Price_store import Price_store
from Aggregator import Aggregator
import websocket
import rel
import time
import signal as sys_signal
from threading import Event

evt = Event()
def handl():
    evt.set()
    rel.abort()
    print('Exit')


agg = Aggregator(evt)
prices = agg.get_price_store()

# websocket.enableTrace(True)
with ThreadPoolExecutor() as executor:
    f1 = executor.submit(initializeBinance, rel, prices)
    f2 = executor.submit(initializeFTX, rel, prices)
    f3 = executor.submit(initializeHuobi, rel, prices)
    f5 = executor.submit(agg.calculate)
    rel.signal(2, handl)  # Keyboard Interrupt
    rel.dispatch()
