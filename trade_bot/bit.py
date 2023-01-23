import bitmex

import second
import datetime
import requests
import json
class Tradebot:
    def __init__(self,syb,price,order,token,id):
        self.price=price
        self.order=order
        self.SYMBOL=syb
        self.token=token
        self.id=id
    def bitmex_(self):
        self.Api = "PKzGWrAmsNU7VkRjDncGUZjX"
        self.Secret = "IA9ScGwXy-qKTj5sSRP20S2wsdr_ODeewupgUNsKWp5JvI7Q"
        self.client = bitmex.bitmex(test=True, api_key=self.Api, api_secret=self.Secret)
        try:
            self.ans=self.client.Order.Order_new(symbol=self.SYMBOL, orderQty=self.order, price=self.price).result()
            self.ans=self.ans[0]
            self.ans['status']=True
            self.ans['id']=2
            data=requests.post(url='http://127.0.0.1:8000/user_exchanges/bit',data=self.ans,headers={'Authorization':'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data=data.json()
            print(data)
        except:
            if self.order<0:
                self.mode='SELL'
            else:
                self.mode='BUY'
            data={'id':2,'status':False,'message':'Request not completed','side':self.mode,'symbol':self.SYMBOL,'quantity':abs(self.order),'time':str(datetime.datetime.now()),'Exchange_name':'Bitmex'}
            data=requests.post(url='http://127.0.0.1:8000/user_exchanges/bit',data=data,headers={'Authorization':'Token 296d8d6136d8bc6ca50813464aee893fc8f37e1f'})
            data=data.json()
            print(data)
        #return self.ans