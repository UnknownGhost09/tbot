from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import websocket
import requests
import scheduler_
import datetime
class TradeBot:
    def __init__(self, symbol, side, size, token,id,api_key,secret_key,passphrase,socket):
        self.symbol = symbol
        self.side = side
        self.size = size
        self.token = token
        self.id=id
        self.api_key = api_key
        self.secret_key = secret_key
        self.socket=str(socket)+self.symbol
        self.passphrase=passphrase
        self.client = Client(self.api_key, self.secret_key, self.passphrase)
        print(self.api_key,self.secret_key,self.id,self.size)
        if self.side == 'sell':
            self.side_ = Client.SIDE_SELL
        elif self.side == 'buy':
            self.side_ = Client.SIDE_BUY
        self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                    on_error=self.on_error, on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self,ws,message):
        print("Message recieved")
        try:
            order = self.client.create_market_order(self.symbol, side=self.side, size=self.size)
            print(order)
            order['id']=self.id
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/kuk', data=order,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            self.ws.close()
        except KucoinAPIException as e:
            scheduler_.cancel_job()
            data = {'id': self.id, 'status': False, 'message': str(e), 'side': self.side, 'symbol': self.symbol,
                    'quantity': self.size, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Kucoin'}
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/kuk', data=data,
                                 headers={'Authorization': self.token})
            data = data.json()
            print(data)
            self.ws.close()

    def on_open(self,*args):
        print("Connection Opened")

    def on_close(self,*args):
        print("Connection close",args)

    def on_error(self, *args):

        print("Here is an error:", args)














