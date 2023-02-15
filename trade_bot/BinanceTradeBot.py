import websocket
import json
from binance.exceptions import BinanceAPIException
from binance.client import Client

import scheduler_
import requests
import datetime
repeat = 'Once'
class TradeBot:
    def __init__(self, s, mode, limit, amount, token,id,api_key,secret_key,socket):
        self.limit = limit
        self.SYMBOL =s
        self.mode = mode
        self.amount = amount
        self.token = token
        self.id=id
        self.socket = socket + self.SYMBOL.lower() + "@kline_1m"
        self.API_KEY = api_key
        self.SECRET_KEY = secret_key
        #print(self.API_KEY,self.SECRET_KEY,self.socket,self.amount)
        print(self.token)
        self.client = Client(self.API_KEY, self.SECRET_KEY, testnet=True)
        self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                    on_error=self.on_error, on_message=self.on_message)
        self.ws.run_forever()
    def on_open(self,*args):
        print("Connection Opened")

    def on_close(self,*args):
        print("Connection close")

    def on_error(self,ws, *args):
        print("Here is an error:", args)
        self.ws.close()

    def on_message(self, ws,*args):
        try:
            self.my_order = self.client.create_order(symbol=self.SYMBOL.upper(),
                                                     side=self.mode, type=self.client.ORDER_TYPE_MARKET,
                                                     quantity=self.amount)
            self.my_order['status'] = True
            self.my_order['id'] = self.id
            self.abc = self.my_order.get('fills')
            self.my_order.pop('selfTradePreventionMode')
            self.my_order.pop('fills')
            result = requests.post(url=' http://192.168.18.110:8000/user_exchanges/bin', data=self.my_order,
                                  headers={'Authorization': self.token})
            result = result.json()
            print(result)

            for i in self.abc:
                i['clientOrderId'] = str(self.my_order.get('clientOrderId'))
                result = requests.post(url='http://192.168.18.110:8000/user_exchanges/fills', data=i,
                                     headers={'Authorization': self.token})
                result = result.json()
                print(result)
            self.ws.close()

        except BinanceAPIException as e:

            data = {'id': self.id, 'status': False, 'message': str(e), 'side': self.mode, 'symbol': self.SYMBOL,
                    'quantity': self.amount, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Binance'}

            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/bin', data=data,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            self.ws.close()
            scheduler_.cancel_job()
