import websocket
import json
from binance.exceptions import BinanceAPIException
from binance.client import Client
import pandas as pd
import requests
import datetime
from dotenv import load_dotenv
from pathlib import Path
import os

class TradeBot:
    def __init__(self,side,amount,symbol,apikey,secretkey,id,token):
        path = Path("./config.env")
        load_dotenv(dotenv_path=path)
        self.SITE_URL = os.getenv('SITE_URL')
        self.SYMBOL = symbol
        self.amount = amount
        self.mode = side
        self.token=token
        self.socket = "wss://stream.binance.com:9443/ws/" + self.SYMBOL.lower() + "@kline_1m"
        self.API_KEY = apikey
        self.SECRET_KEY = secretkey
        self.id=id
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
            self.my_order = json.dumps(self.my_order)
            data={"id":self.id,"order":self.my_order}
            data = requests.post(url=self.SITE_URL + '/user_exchanges/logs', data=data,
                                 headers={'Authorization': self.token})
            data = data.json()

            with open(r'binancelogs.json','a') as fl:
                fl.write(self.my_order+",")
            ws.close()

        except BinanceAPIException as e:
            print(e)
            ws.close()









