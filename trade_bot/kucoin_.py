from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import websocket
import requests
import scheduler_
import datetime
class TradeBot:
    def __init__(self, symbol, side, size, token,id,api_key,secret_key,socket,passphrase):
        self.symbol = symbol
        self.side = side
        self.size = size
        self.token = token
        self.id=id
        self.api_key = "63c10b64d3c0b80001976a4a"
        self.secret_key = "5462283a-15d3-4c32-85e4-f24a00bc8c27"
        self.socket="wss://ws-api.kucoin.com/endpoint/market/ticker:"+self.symbol
        self.passphrase="Urveesh@123"
        self.client = Client(self.api_key, self.secret_key, self.passphrase)
        if self.side == 'sell':
            self.side_ = Client.SIDE_SELL
        elif self.side == 'buy':
            self.side_ = Client.SIDE_BUY
        self.ws = websocket.WebSocketApp(self.socket, on_open=on_open, on_close=on_close,
                                    on_error=on_error, on_message=self.on_message)

        self.ws.run_forever()

    def on_message(self,ws, error):
        print("Message recieved")
        try:
            order = self.client.create_market_order(self.symbol, side=self.side, size=self.size)
            order['id']=1
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/kuk', data=order)
            data = data.json()
            print(data)
            ws.close()
        except KucoinAPIException as e:
            scheduler_.cancel_job()
            data = {'id': 1, 'status': False, 'message': str(e), 'side': self.side, 'symbol': self.symbol,
                    'quantity': self.size, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Kucoin'}
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/kuk', data=data,
                                 headers={'Authorization': 'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data = data.json()
            print(data)
            ws.close()

def on_open(ws):
    print("Connection Opened")

def on_close(ws,*args):
    print("Connection close",args)

def on_error(ws, error):
    print("Here is an error:", error)














