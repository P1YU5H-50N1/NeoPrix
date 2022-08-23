import websocket
from websocket import WebSocketApp
from websocket._abnf import ABNF
import sys
from datetime import datetime 
import json


def on_message(ws, message):
    # print('BINANCE')
    message = json.loads(message)
    if not 's' in message.keys():
        # print(message)
        return
    else:
        time, market, price = message['E'], message['s'], message['p']
        ws.price.add(time, price, market,'BINANCE')

def on_error(ws, error):
    print("BINANCE ERR", error)
    sys.exit()

def on_close(ws, close_status_code, close_msg):
    subscribe = {
        "method": "UNSUBSCRIBE",
        "params":
        [
            "btcusdt@trade",
            "ethusdt@trade",
            "maticusdt@trade"
        ],
        "id": 1
    }
    payload = json.dumps(subscribe)
    ws.send(payload)
    print("### closed ###")


def on_ping(ws, msg):
    print(msg)
    ws.send(msg, ABNF.OPCODE_PONG)


def on_open(ws):
    print("Opened connection")
    subscribe = {
        "method": "SUBSCRIBE",
        "params":
        [
            "btcusdt@aggTrade",
            "ethusdt@aggTrade",
            "maticusdt@aggTrade"
        ],
        "id": 1
    }
    payload = json.dumps(subscribe)
    ws.send(payload)


class Binance(WebSocketApp):

    def __init__(self, rel, price):
        self.price = price
        super().__init__("wss://stream.binance.com:9443/ws",
                         on_open=on_open,
                         on_ping=on_ping,
                         on_message=on_message,
                         on_error=on_error,
                         on_close=on_close)
        super().run_forever(ping_interval=10, dispatcher=rel)


def initializeBinance(rel, price):
    client = Binance(rel, price)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = Binance()
