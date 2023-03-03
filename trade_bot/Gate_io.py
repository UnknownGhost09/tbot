import hashlib
import hmac
import json
import logging
import time
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from gate_api import SpotApi, MarginApi, WalletApi, ApiClient, Order
import requests

import datetime
# pip install -U websocket_client
from websocket import WebSocketApp
logging.basicConfig(level=logging.INFO)
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TradeBot:
    def __init__(self,symbol,side,price,amount,token,id,api_key,secret_key,socket,**kwargs):
        self.symbol=symbol.upper()
        self.side=side
        self.price=price
        self.amount=amount
        self.token=token
        self.id=id
        self._api_key = api_key
        self._secret_key = secret_key
        self.socket=socket
    def global_(self):
        global symbol
        global side
        global price
        global amount
        global token
        global id
        global _api_key
        global _secret_key
        global socket
        global config
        global logger
        global spot_api
        global ws
        symbol = self.symbol
        print(symbol)
        side=self.side
        print(side)
        price=self.price
        print(price)
        amount = self.amount
        print(amount)
        token = self.token
        print(token)
        id = self.id
        print(id)
        _api_key = self._api_key
        print(_api_key)
        _secret_key = self._secret_key
        print(_secret_key)
        socket= self.socket
        print(socket)

        config = gate_api.Configuration(
            key=_api_key,
            secret=_secret_key
        )
        spot_api = SpotApi(ApiClient(config))
        ws=GateWebSocketApp(socket,
                             _api_key,
                             _secret_key,
                             on_open=on_open,
                             on_message=on_message)
        ws.run_forever(ping_interval=5)
class GateWebSocketApp(WebSocketApp):

    def __init__(self, url, api_key, api_secret, **kwargs):
        super(GateWebSocketApp,self).__init__(url,**kwargs)
        self._api_key = api_key
        self._api_secret = api_secret

    def _send_ping(self,*args):
        pass

    def _request(self, channel, event=None, payload=None, auth_required=True):
        current_time = int(time.time())
        data = {
            "time": current_time,
            "channel": channel,
            "event": event,
            "payload": payload,
        }
        if auth_required:
            message = 'channel=%s&event=%s&time=%d' % (channel, event, current_time)
            data['auth'] = {
                "method": "api_key",
                "KEY": self._api_key,
                "SIGN": self.get_sign(message),
            }
        data = json.dumps(data)
        logger.info('request: %s', data)
        self.send(data)
    def get_sign(self, message):
        h = hmac.new(self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
        return h.hexdigest()

    def subscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "subscribe", payload, auth_required)

    def unsubscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "unsubscribe", payload, auth_required)
def on_message(ws, message,*args):
    # type: (TradeBot, str) -> None
    # handle whatever message you received
    print("message recived")
    logger.info("message received from server: {}".format(message))

    try:
        order = Order(account='margin', currency_pair=symbol,price=price,
                      amount=amount, side=side)
        order =spot_api.create_order(order)
        ws.close()
        order['id']=id
        exchanges = json.dumps(order)
        print(order)

        with open(r'tradedata.json', 'a') as fl:
            fl.write(",")
            fl.write(exchanges)
        data = requests.post(url='http://192.168.18.110:8000/user_exchanges/gate', data=order,
                             headers={'Authorization': token})

        data = data.json()
        print(data)

    except GateApiException as e:
        data = {'id': id, 'status': False, 'message': str(e), 'side': side, 'symbol': symbol,
                'quantity': amount, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Gateio'}
        if 'Not enough balance' in data['message'] or 'NOT ENOUGH BALANCE' in data['message'] or 'insufficent Balance' in data['message'] or "INSUFFICIENT BALANCE" in data['messsage'] or 'BALANCE_NOT_ENOUGH' in data['message']:
            data['message'] = 'Not enough balance'
        exchanges = json.dumps(data)
        print(e)
        ws.close()
        with open(r'tradedata.json', 'a') as fl:
            fl.write(",")
            fl.write(exchanges)

        data = requests.post(url='http://192.168.18.110:8000/user_exchanges/gate', data=data,
                             headers={'Authorization': token})
        data = data.json()
        print(data)

def on_open(ws):
    # type: #(TradeBot) -> None
    print("connection oppended")
    logger.info('websocket  connected')
    ws.subscribe("spot.trades", [symbol], False)
#token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJveEBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImJveCIsImV4cCI6MTY4MDA4MjYwMX0.at2VCpus4HEQLQzhhl99GKoDf4HM5ivMYNQyznqG_GY'
#api_key = '996fe20df5af3f7a53ce291b6e46a975'
#secret_key = '41492892a8000de41686021ca2afd390f472731715da5020d29f0f5180ae8f53'

#socket = 'wss://api.gateio.ws/ws/v4/'

#obj=TradeBot("BTC_USDT","buy",23000,1,token,1,api_key,secret_key,socket)
#obj.global_()


