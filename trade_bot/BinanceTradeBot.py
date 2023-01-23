
import json
from binance.exceptions import BinanceAPIException
# from binance.spot import Spot as Client
from binance.client import Client
# from binance.enums import *
import pandas as pd
import second
import json
import requests
import json
import datetime
class TradeBot:
    def __init__(self, s, mode, limit, amount, token,id):
        self.limit = limit
        self.SYMBOL = s
        self.mode = mode
        self.amount = amount
        self.token = token
        self.id=id

    def Binance(self):
        self.socket = "wss://stream.binance.com:9443/ws/" + self.SYMBOL.lower() + "@kline_1m"
        self.API_KEY = '7gr7eBfTq9IqaexFkjRVje17t8dTLjE30fck2oVucTURRqOqlYULW8xnKh8rMiZR'
        self.SECRET_KEY = 'Ai6F7MpVZvHQBHC0Yb07Djs5I2bmjUqsRVgssjPn3UzcviVn8VbSg5L3ZiC3pYjM'
        self.client = Client(self.API_KEY, self.SECRET_KEY, testnet=True)
        try:
            self.my_order = self.client.create_order(symbol=self.SYMBOL.upper(),
                                                     side=self.mode, type=self.client.ORDER_TYPE_MARKET,
                                                     quantity=amount)

            self.my_order['status'] = True
            self.my_order['id'] = 2
            self.abc = self.my_order.get('fills')
            self.my_order.pop('selfTradePreventionMode')
            self.my_order.pop('fills')
            data = requests.post(url='http://127.0.0.1:8000/user_exchanges/bin', data=self.my_order,
                                 headers={'Authorization': 'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data = data.json()
            print(data)

            for i in self.abc:
                i['clientOrderId'] = str(self.my_order.get('clientOrderId'))
                data = requests.post(url='http://127.0.0.1:8000/user_exchanges/fills', data=i,
                                     headers={'Authorization': 'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
                data = data.json()
                print(data)


        except BinanceAPIException as e:
            data = {'id': 2, 'status': False, 'message': str(e), 'side': self.mode, 'symbol': self.SYMBOL,
                    'quantity': self.amount, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Binance'}

            data = requests.post(url='http://127.0.0.1:8000/user_exchanges/bin', data=data,
                                 headers={'Authorization': 'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data = data.json()
            print(data)


amount = 0.5  # need to change amount




