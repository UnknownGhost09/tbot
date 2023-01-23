
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from gate_api import SpotApi,MarginApi,WalletApi,ApiClient,Order
import datetime
import requests
class TradeBot:
    def __init__(self,symbol,side,price,amount,token,id):
        self.symbol=symbol
        self.side=side
        self.price=price
        self.amount=amount
        self.token=token
        self.id=id
    def gateio_(self):

        self.config = gate_api.Configuration(
            host = "https://api.gateio.ws/api/v4",
            key = "996fe20df5af3f7a53ce291b6e46a975",
            secret = "41492892a8000de41686021ca2afd390f472731715da5020d29f0f5180ae8f53"
        )

        self.spot_api = SpotApi(ApiClient(self.config))
        try:
            self.order = Order(account='margin', currency_pair=self.symbol, price=self.price, amount=self.amount,
                      side=self.side)
            self.orders = self.spot_api.create_order(self.order)
            data=requests.post(url='http://127.0.0.1:8000/user_exchanges/gate',data=self.orders,headers={'Authorization':'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data=data.json()
            print(data)
        except GateApiException as e:
            data={'id':2,'status':False,'message':str(e),'side':self.side,'symbol':self.symbol,'quantity':self.amount,'time':str(datetime.datetime.now()),'Exchange_name':'Gate.io'}
            data=requests.post(url='http://127.0.0.1:8000/user_exchanges/gate',data=data,headers={'Authorization':'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data=data.json()
            print(data)













