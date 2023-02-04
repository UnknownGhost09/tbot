import hashlib
import hmac
import json
import logging
import time
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from gate_api import SpotApi, MarginApi, WalletApi, ApiClient, Order
import requests
import scheduler_
import datetime
# pip install -U websocket_client
from websocket import WebSocketApp

class TradeBot:
    def __init__(self,symbol,side,price,amount,token,id,api_key,secret_key,socket,**kwargs):
        #super(TradeBot, self).__init__(url, **kwargs)
        self.symbol=symbol.upper()
        self.side=side
        self.price=price
        self.amount=amount
        self.token=token
        self.id=id
        self._api_key = api_key
        self._secret_key = secret_key
        self.socket=socket
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.config = gate_api.Configuration(
            key="996fe20df5af3f7a53ce291b6e46a975",
            secret="41492892a8000de41686021ca2afd390f472731715da5020d29f0f5180ae8f53"
        )
        self.spot_api = SpotApi(ApiClient(self.config))
        logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
        app = GateWebSocketApp("wss://api.gateio.ws/ws/v4/",
                               "996fe20df5af3f7a53ce291b6e46a975",
                               "41492892a8000de41686021ca2afd390f472731715da5020d29f0f5180ae8f53",
                               self.logger,
                               self.config,
                               self.spot_api,
                               on_open=self.on_open,
                               on_message=self.on_message)
        app.run_forever(ping_interval=5)

    def on_open(self,ws):
        # type: (TradeBot) -> None
        # subscribe to channels interested
        self.logger.info('websocket connected')
        ws.subscribe("spot.trades", [self.symbol], False)

    def on_message(self,ws, message):
        # type: (TradeBot, str) -> None
        # handle whatever message you received
        self.logger.info("message received from server: {}".format(message))
        try:
            self.order = Order(account='margin', currency_pair=self.symbol,price=self.price,
                          amount=self.amount, side=self.side)

            self.order =self.spot_api.create_order(self.order)
            self.order['id']=1
            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/gate', data=self.order)
            data = data.json()
            print(data)
            ws.close()
        except GateApiException as e:

            scheduler_.cancel_job()
            data = {'id': 1, 'status': False, 'message': str(e), 'side': self.side, 'symbol': self.symbol,
                    'quantity': self.amount, 'time': str(datetime.datetime.now()), 'Exchange_name': 'Binance'}

            data = requests.post(url='http://192.168.18.110:8000/user_exchanges/gate', data=data)
            data = data.json()
            print(data)
            ws.close()

class GateWebSocketApp(WebSocketApp):

    def __init__(self, url, api_key, api_secret,logger,config,spot_api, **kwargs):
        super(GateWebSocketApp, self).__init__(url, **kwargs)
        self._api_key = api_key
        self._api_secret = api_secret
        self.logger=logger
        self.config=config
        self.spot_api=spot_api

    def _send_ping(self):
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
        self.logger.info('request: %s', data)
        self.send(data)

    def get_sign(self, message):
        h = hmac.new(self._api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
        return h.hexdigest()

    def subscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "subscribe", payload, auth_required)

    def unsubscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "unsubscribe", payload, auth_required)


























