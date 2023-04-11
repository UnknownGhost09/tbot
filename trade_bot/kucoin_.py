from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import requests
import datetime
import json
import websocket
from websocket import WebSocketApp
import os
from dotenv import load_dotenv
from pathlib import Path


class TradeBot:
    def __init__(self, symbol, side, amount, token, id, api_key, secret_key, passphrase, socket):
        path = Path("./config.env")
        load_dotenv(dotenv_path=path)
        self.SITE_URL = os.getenv('SITE_URL')
        self.symbol = symbol
        self.side = side
        self.amount = amount
        self.token = token
        self.id = id
        print(self.id)
        self.api_key = api_key
        self.secret_key = secret_key
        self.socket = str(socket) + self.symbol
        self.passphrase = passphrase
        self.client = Client(self.api_key, self.secret_key, self.passphrase)
        # print(self.api_key,self.secret_key,self.id,self.size)
        if self.side == 'sell':
            self.side_ = Client.SIDE_SELL
            print(self.side_)
        elif self.side == 'buy':
            self.side_ = Client.SIDE_BUY
            print(self.side_)
        ws =WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                         on_error=self.on_error, on_message=self.on_message)
        ws.run_forever()

    def on_message(self,ws, message):
        print("Message recieved")
        try:
            order = self.client.create_market_order(self.symbol, side=self.side_, size=self.amount)
            print(order)

            order['id'] = self.id
            exchanges = json.dumps(order)
            with open(r'tradedata.json', 'a') as fl:
                fl.write(",")
                fl.write(exchanges)
            order['flag']='True'
            data = requests.post(url=self.SITE_URL+'/user_exchanges/kuk', data=order,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            logs = {'id': self.id, 'symbol': self.symbol,
                    'price': '',
                    'quantity': self.amount, 'side': self.side_, 'exchange': 'Kucoin'}
            data = requests.post(url=self.SITE_URL + '/user_exchanges/logs', data=logs,
                                 headers={'Authorization': self.token})

            data = data.json()
            print(data)
            ws.close()
        except KucoinAPIException as e:
            print(e)

            data = {'id': self.id, 'status': False, 'message': 'Balance not found', 'side': self.side_, 'symbol': self.symbol,
                    'quantity': self.amount, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Kucoin'}
            print(data)

            exchanges = json.dumps(data)
            print(exchanges)

            with open(r'tradedata.json', 'a') as fl:
                fl.write(",")
                fl.write(exchanges)
            data = requests.post(url=self.SITE_URL+'/user_exchanges/kuk', data=data,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            ws.close()
    def on_open(self,*args):
        print("Connection Opened")
    def on_close(self,*args):
        print("Connection close")
    def on_error(self,ws,error):

        print("Here is an error:", error)
        ws.close()

