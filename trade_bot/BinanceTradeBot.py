import websocket
import json
from binance.exceptions import BinanceAPIException
from binance.client import Client
import pandas as pd
import scheduler_
import requests
import datetime
amount = 0.01
repeat = 'Once'
class TradeBot:
    def __init__(self, s, mode, limit, amount, token,id,api_key,secret_key,socket):
        self.limit = limit
        self.SYMBOL =s
        self.mode = mode
        self.amount = amount
        self.token = token
        self.id=id
        self.api_key=api_key
        self.secret_key=secret_key
        self.socket = "wss://stream.binance.com:9443/ws/" + self.SYMBOL.lower() + "@kline_1m"
        self.API_KEY = '7gr7eBfTq9IqaexFkjRVje17t8dTLjE30fck2oVucTURRqOqlYULW8xnKh8rMiZR'
        self.SECRET_KEY = 'Ai6F7MpVZvHQBHC0Yb07Djs5I2bmjUqsRVgssjPn3UzcviVn8VbSg5L3ZiC3pYjM'
        self.client = Client(self.API_KEY, self.SECRET_KEY, testnet=True)
        ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                    on_error=self.on_error, on_message=self.on_message)
        ws.run_forever()
    def on_open(self,ws):
        print("Connection Opened")

    def on_close(self,ws):
        print("Connection close")

    def on_error(self,ws, error):
        print("Here is an error:", error)

    def on_message(self,ws, message):
        try:
            self.my_order = self.client.create_order(symbol=self.SYMBOL.upper(),
                                                     side=self.mode, type=self.client.ORDER_TYPE_MARKET,
                                                     quantity=amount)
            self.my_order['status'] = True
            self.my_order['id'] = 1
            self.abc = self.my_order.get('fills')
            self.my_order.pop('selfTradePreventionMode')
            self.my_order.pop('fills')
            data = requests.post(url=' http://192.168.18.110:8000/user_exchanges/bin', data=self.my_order)
            data = data.json()
            print(data)

            for i in self.abc:
                i['clientOrderId'] = str(self.my_order.get('clientOrderId'))
                data = requests.post(url='http://192.168.18.110:8000/user_exchanges/bin', data=i)
                data = data.json()
                print(data)
            ws.close()

        except BinanceAPIException as e:
            scheduler_.cancel_job()
            data = {'id': 1, 'status': False, 'message': str(e), 'side': self.mode, 'symbol': self.SYMBOL,
                    'quantity': self.amount, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Binance'}

            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/bin', data=data)
            data = data.json()
            print(data)
            ws.close()
