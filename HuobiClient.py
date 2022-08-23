import websocket
from websocket import WebSocketApp
from websocket._abnf import ABNF
import gzip
from datetime import datetime
import sys
import json


def decompress(message):
    if isinstance(message, (str)):
        dict_data = json.loads(message)
    elif isinstance(message, (bytes)):
        dict_data = json.loads(gzip.decompress(message).decode("utf-8"))
    else:
        print("RX unknow type : ", type(message))
        return message
    return dict_data


def on_message(ws, message):
    # print("HUOBI")
    # global prices
    dict_data = decompress(message)
    if "ping" in dict_data.keys():
        pong_payload = json.dumps({"pong": dict_data["ping"]})
        # print(pong_payload)
        ws.send(pong_payload)
    elif "ch" in dict_data.keys():
        market = dict_data["ch"]
        times = []
        prices = []
        for i in dict_data["tick"]["data"]:
            time, price = i["ts"], i["price"]
            times.append(time / 100)
            prices.append(price)
            ws.prices.add(time, price, market, "HUOBI")
    elif "status" in dict_data.keys():
        print("Subscribtion successful", dict_data["subbed"])
    else:
        print(dict_data)


def on_error(ws, error):

    print("HUOBI ERR", type(error), error)
    sys.exit()


def on_close(ws, close_status_code, close_msg):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("CLOSE TIME =", current_time)
    print("### closed ###")


def on_open(ws):
    print("Opened connection")

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("OPEN TIME =", current_time)
    subscribe = [
        {"sub": "market.btcusdt.trade.detail", "id": "id1"},
        {"sub": "market.maticusdt.trade.detail", "id": "id1"},
        {"sub": "market.ethusdt.trade.detail", "id": "id1"},
    ]
    for sub in subscribe:
        payload = json.dumps(sub)
        ws.send(payload)


class Huobi(WebSocketApp):
    def __init__(self, rel, price_store):
        self.prices = price_store
        super().__init__(
            "wss://api.huobi.pro/ws",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
        super().run_forever(dispatcher=rel)


def initializeHuobi(rel, price_store):
    client = Huobi(rel, price_store)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = Huobi()
    print(ws.__class__)

# Heartbeat
# {
#     "action": "ping",
#     "data": {
#         "ts": 1575537778295
#     }
# }
# Once the Websocket connection is established, Huobi server will periodically send "ping" message at 20s interval, with an integer inside.

# {
#     "action": "pong",
#     "data": {
#           "ts": 1575537778295 // the same with "ping" message
#     }
# }
# Once client receives "ping", it should respond "pong" message back with the same integer.
