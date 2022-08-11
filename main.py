from concurrent.futures import ThreadPoolExecutor
from BinanceClient import initializeBinance
from FTXClient import initializeFTX
from HuobiClient import initializeHuobi
from Price_store import Price_store
import rel
import time
import signal as sys_signal
from threading import Event

def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)
        
def print_price(prices,evt):
        while True:
            if evt.is_set():
                return
            print(prices)
        # clear_line(len(prices))
        
evt = Event()
prices = Price_store()
def handl():
    evt.set()
    rel.abort()
    print('Exit')


with ThreadPoolExecutor(max_workers=4) as executor:
    f1 = executor.submit(initializeBinance,rel,prices)
    f2 = executor.submit(initializeFTX,rel,prices)
    f3 = executor.submit(initializeHuobi,rel,prices)
    f4 = executor.submit(print_price,prices,evt)
    # print(f3.result())
    s = rel.signal(2, handl) # Keyboard Interrupt
    # print("report",rel.report())
    # # time.sleep(2)
    # s.delete()
    # print("report",rel.report())
    
    # print(f4.result())
    rel.dispatch()

