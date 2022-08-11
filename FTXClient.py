import websocket
from websocket import WebSocketApp
import json

def on_message(ws, message):
    # print("FTX")
    message = json.loads(message)
    market = message['market']
    if not 'data' in message.keys():
       print("FTX Subscription successfull")
    else:
        for info in message['data']:
            
            # print(f"FTx       {info['time']}    {market}  {info['price']}")
            ws.prices.add(info['time'],info['price'],market)
        

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    unsubscribe = ['{"op": "unsubscribe", "channel": "trades", "market": "BTC/USD"}',
                 '{"op": "unsubscribe", "channel": "trades", "market": "ETH/USD"}',
                 '{"op": "unsubscribe", "channel": "trades", "market": "MATIC/USD"}'
                 ]
    for crypto in unsubscribe:
        ws.send(crypto)
    print("### closed ###")

def on_ping(ws):
    ws.send('{"op": "ping"}') 

def on_open(ws):
    subscribe = ['{"op": "subscribe", "channel": "trades", "market": "BTC/USD"}',
                 '{"op": "subscribe", "channel": "trades", "market": "ETH/USD"}',
                 '{"op": "subscribe", "channel": "trades", "market": "MATIC/USD"}'
                 ]
    print("Opened connection")
    for crypto in subscribe:
        ws.send(crypto)
   
    
class FTXClient(WebSocketApp):
    def __init__(self,rel,prices):
        self.prices = prices
        super().__init__("wss://ftx.com/ws/",
                            on_open=on_open,
                            on_ping = on_ping,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
        super().run_forever(ping_interval=10,dispatcher=rel)

def initializeFTX(rel,prices):
    client = FTXClient(rel,prices)
    


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = FTXClient()