from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import websocket
import requests

import datetime
import json


class TradeBot:
    def __init__(self, symbol, side, amount, token, id, api_key, secret_key, passphrase, socket):
        self.symbol = symbol
        self.side = side
        self.amount = amount
        self.token = token
        self.id = id
        self.api_key = api_key
        self.secret_key = secret_key
        self.socket = str(socket) + self.symbol
        self.passphrase = passphrase
        self.client = Client(self.api_key, self.secret_key, self.passphrase)
        # print(self.api_key,self.secret_key,self.id,self.size)
        if self.side == 'sell':
            self.side_ = Client.SIDE_SELL
        elif self.side == 'buy':
            self.side_ = Client.SIDE_BUY
        self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                         on_error=self.on_error, on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, ws, message):
        print("Message recieved")
        try:
            order = self.client.create_market_order(self.symbol, side=self.side, size=self.amount)
            print(order)

            order['id'] = self.id
            exchanges = json.dumps(order)
            with open(r'tradedata.json', 'a') as fl:
                fl.write(",")
                fl.write(exchanges)
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/kuk', data=order,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            self.ws.close()
        except KucoinAPIException as e:

            data = {'id': self.id, 'status': False, 'message': str(e), 'side': self.side, 'symbol': self.symbol,
                    'quantity': self.size, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Kucoin'}
            if 'Not enough balance' in data.get('message') or 'NOT ENOUGH BALANCE' in data.get(
                    'message') or 'insufficent Balance' in data.get('message') or "INSUFFICIENT BALANCE" in data.get(
                    'messsage') or 'BALANCE_NOT_ENOUGH' in data.get('message'):
                data['message'] = 'Not enough balance'
            exchanges = json.dumps(data)
            with open(r'tradedata.json', 'a') as fl:
                fl.write(",")
                fl.write(exchanges)
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/kuk', data=data,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            self.ws.close()

    def on_open(self, *args):
        print("Connection Opened")

    def on_close(self, *args):
        print("Connection close", args)

    def on_error(self, *args):

        print("Here is an error:", args)
        self.ws.close()