from concurrent.futures import ThreadPoolExecutor
from BinanceClient import initializeBinance
from FTXClient import initializeFTX
from HuobiClient import initializeHuobi
import rel



with ThreadPoolExecutor() as executor:
    f1 = executor.submit(initializeBinance,rel)
    f2 = executor.submit(initializeFTX,rel)
    f3 = executor.submit(initializeHuobi,rel)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

