import requests
import json
import pandas as pd 
import numpy as np
import time
def fxn3(i):
    if 'last' in i.columns:
        a=i.loc[i['symbol_name']==syb,['last','exchange_name','symbol']]
        a.rename(columns={'last':'price'},inplace=True)
        a.reset_index(inplace=True,drop=True)
        return a
    elif 'price' in i.columns:
        a=i.loc[i['symbol_name']==syb,['price','exchange_name','symbol']]
        a.reset_index(inplace=True,drop=True)
        return a
    elif 'lastTradeRate' in i.columns:
        a=i.loc[i['symbol_name']==syb,['lastTradeRate','exchange_name','symbol']]
        a.rename(columns={'lastTradeRate':'price'},inplace=True)
        a.reset_index(inplace=True,drop=True)
        return a
    elif 'rate' in i.columns:
        a=i.loc[i['symbol_name']==syb,['rate','exchange_name','symbol']]
        a.rename(columns={'rate':'price'},inplace=True)
        a.reset_index(inplace=True,drop=True)
        return a
def fxn(i):
    if type(lst[i])==dict:
        if 'ticker' in lst[i]:
            abcd=pd.DataFrame(lst[i]['ticker'])
            abcd['symbol_name']=abcd['symbol'].str.replace('-','').str.replace('_','')
            abcd['exchange_name']=lst1[i].get('exchange_name')
            return abcd
            
        elif 'data' in lst[i]:
            if 'ticker' in lst[i]['data']:
                #abcd=list(map(fxn2,lst[i]['data']['ticker']))
                abcd=pd.DataFrame(lst[i]['data']['ticker'])
                abcd['symbol_name']=abcd['symbol'].str.replace('-','').str.replace('_','')
                abcd['exchange_name']=lst1[i].get('exchange_name')
                return abcd
            else:
                txt=pd.DataFrame(lst[i]['data'])
                txt=txt.drop(['symbol'],axis=1)
                txt['symbol']=txt['pair']
                txt=txt.drop(['pair'],axis=1)
                txt['symbol_name']=txt['symbol'].str.replace('_','').str.upper()
                txt['exchange_name']=lst1[i].get('exchange_name')
                return txt            
        else:
            keys=list(lst[i].keys())
            values=list(lst[i].values())
            for j in range(len(keys)):
                values[j]['symbol_name']=keys[j].replace('_','').upper()
                values[j]['symbol']=keys[j]
            abcd=pd.DataFrame(values)
            abcd['exchange_name']=lst1[i].get('exchange_name')
            return abcd
    if type(lst[i])==list:
        
        #abcd=list(map(fxn2,lst[i]))
        abcd=pd.DataFrame(lst[i])
        abcd['symbol_name']=abcd['symbol'].str.replace('-','').str.replace('_','')
        abcd['exchange_name']=lst1[i].get('exchange_name')
        return abcd
def fxn4(i):
    i=i.replace('_','')
    if 'XBT' in i:
        return i.replace('XBT','BTC')
    else:
        return i 

class First:
    def __init__(self,symbol):
        self.syb=symbol
    def coin(self):
        global lst
        global lst1
        global syb
        syb=self.syb
        with open(r'config.json','r') as fl:
            lst=fl.read()
        lst1=json.loads(lst).get('Exchanges')
        lst=[requests.get(i.get('Symbol')).json() for i in lst1 if i.get('exchange_name')!='Bitmex']
        bit_symbol=[i.get('Symbol') for i in lst1 if i.get('exchange_name')=='Bitmex']
        bit_max=[requests.get(i.get('Symbol')).json().get('all') for i in lst1 if i.get('exchange_name')=='Bitmex']
        lst1=[i for i in lst1 if i.get('exchange_name')!='Bitmex']
        if len(bit_max)>0 and len(bit_symbol)>0:
            bit_max=bit_max[0]
            bit_symbol=bit_symbol[0]
            if bit_max!=None:
                bit_max2=list(map(fxn4,bit_max))
                if syb in bit_max2:
                    sy=bit_max[bit_max2.index(syb)]
                    bit_symbol+=sy+'/trades'
                    bit_data=requests.get(url=bit_symbol).json()[-1]
                else:
                    bit_data=None
                    del bit_symbol
                    del bit_max
            else:
                bit_data=None
                del bit_symbol
                del bit_max
        else:
            bit_data=None
            del bit_symbol
            del bit_max
        self.result=list(map(fxn,range(len(lst))))        
        self.result=list(map(fxn3,self.result))
        self.result=[[float(i.loc[0,'price']),i.loc[0,'exchange_name'],i.loc[0,'symbol']] for i in self.result if len(i)>0]
        if bit_data!=None:
            self.result.append([float(bit_data.get('price')),'Bitmex',sy])
        #return self.result
        self.result=[min(self.result),max(self.result)]
        return self.result

obj=First('BTCUSDT')
result=obj.coin()







