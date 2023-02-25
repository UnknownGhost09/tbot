import websocket
import json
from binance.exceptions import BinanceAPIException
from binance.client import Client
import pandas as pd

import requests
import datetime

amount = 0.01
repeat = 'Once'
initial = 1


class TradeBot:
    def __init__(self, s, side, amount, token, id, api_key, secret_key, socket):
        self.SYMBOL = s
        self.amount = amount
        self.token = token
        self.id = id
        self.mode = side
        self.api_key = api_key
        self.secret_key = secret_key
        self.socket = str(socket) + self.SYMBOL.lower() + "@kline_1m"
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        self.client = Client(self.API_KEY, self.SECRET_KEY, testnet=True)
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
                                                     quantity=self.amount)
            print(self.my_order)
            self.my_order = json.dumps(self.my_order)
            with open('tradehistory.json', 'a') as fl:
                fl.write(',')
                fl.write(self.my_order)
            ws.close()
        except BinanceAPIException as e:
            print(e)
            data = {'message': 'Failed', 'data': 'Not Enough balance'}
            print(data)
            data = json.dumps(data)
            with open('tradehistory.json', 'a') as fl:
                fl.write(',')
                fl.write(data)
            ws.close()
            # return e
