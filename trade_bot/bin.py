import websocket
import json
from binance.exceptions import BinanceAPIException
from binance.client import Client
import pandas as pd

import requests
import datetime


class TradeBot:
    def __init__(self,side,amount,symbol):
        self.SYMBOL = symbol
        self.amount = amount
        self.mode = side
        self.socket = "wss://stream.binance.com:9443/ws/" + self.SYMBOL.lower() + "@kline_1m"
        self.API_KEY = 'ACebgoy9pnpy0CzbI4xGdeUcVXUaRoO5u5PLKYnz1dp8f4bWlNhS1uhqzxx0Nc1f'
        self.SECRET_KEY = 'VbeLJgHSMC8LVUNwFHRvff8UyFwMmjp90NWNXobKHrEfY2dcSxyY7cRDR0Po89g9'
        self.client = Client(self.API_KEY, self.SECRET_KEY, testnet=False)
        ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                    on_error=self.on_error, on_message=self.on_message)
        ws.run_forever()

    def on_open(self, ws):
        print("Connection Opened")

    def on_close(self, ws):
        print("Connection close")

    def on_error(self, ws, error):
        print("Here is an error:", error)

    def on_message(self, ws, message):
        try:
            self.my_order = self.client.create_order(symbol=self.SYMBOL.upper(),
                                                     side=self.mode, type=self.client.ORDER_TYPE_MARKET,
                                                     quantity=float(self.amount))
            print(self.my_order)
            self.my_order=json.dumps(self.my_order)
            with open(r'binancelogs.json','a') as fl:
                fl.write(self.my_order+",")
            ws.close()

        except BinanceAPIException as e:
            print(e)
            ws.close()




