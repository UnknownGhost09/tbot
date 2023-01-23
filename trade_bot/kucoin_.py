from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException
import datetime
import requests


class TradeBot:
    def __init__(self, symbol, side, size, token,id):
        self.symbol = symbol
        self.side = side
        self.size = size
        self.token = token
        self.id=id

    def kucoin_(self):
        self.api_key = "63c10b64d3c0b80001976a4a"
        self.secret_key = "5462283a-15d3-4c32-85e4-f24a00bc8c27"
        self.passphrase = "Urveesh@123"
        self.client = Client(self.api_key, self.secret_key, self.passphrase)
        if self.side == 'sell':
            self.side_ = Client.SIDE_SELL
        elif self.side == 'buy':
            self.side_ = Client.SIDE_BUY
        try:
            self.order = self.client.create_market_order(self.symbol, self.side_, size=self.size)
            return self.order
        except KucoinAPIException as e:
            data = {'id': 2, 'status': False, 'message': str(e), 'side': self.side, 'symbol': self.symbol,
                    'quantity': self.size, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Kucoin'}
            data = requests.post(url='http://127.0.0.1:8000/user_exchanges/kuk', data=data,
                                 headers={'Authorization': 'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data = data.json()
            print(data)
