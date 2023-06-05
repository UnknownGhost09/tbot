import BinanceTradeBot

import threading
import kucoin_
import Gate_io
import websocket
from binance.exceptions import BinanceAPIException
from binance.client import Client
import pandas as pd
import requests
import second
import os
import bin
from dotenv import load_dotenv
from pathlib import Path
from collections import deque
import talib

running = True
td = True

killorder=0

# def binance_trade(SYMBOL,side, amount, token, id, binapi_key, binsecret_key, bin_socket):
#     bot = BinanceTradeBot.TradeBot(SYMBOL, side, amount, token, id, binapi_key, binsecret_key, bin_socket)
#     return bot


def binance_trade(side,amount,symbol):
    bot = bin.TradeBot(side,amount,symbol)
    return bot

def kucoin_trade(symbol, side, amount, token, id, kucapi_key, kucsecret_key, passphrase, kuk_socket):
    obj = kucoin_.TradeBot(symbol, side, amount, token, id, kucapi_key, kucsecret_key, passphrase, kuk_socket)
    return obj

def gateio_trade(symbol, side, price, amount, token, id, gateapi_key, gatesecret_key, gate_socket):
    obj = Gate_io.TradeBot(symbol, side, price, amount, token, id, gateapi_key, gatesecret_key, gate_socket)
    print(obj)
    return obj

"""class PSAR:

  def __init__(self, init_af=0.02, max_af=0.2, af_step=0.02):
    self.max_af = max_af
    self.init_af = init_af
    self.af = init_af
    self.af_step = af_step
    self.extreme_point = None
    self.high_price_trend = []
    self.low_price_trend = []
    self.high_price_window = deque(maxlen=2)
    self.low_price_window = deque(maxlen=2)

    self.psar_list = []
    self.af_list = []
    self.ep_list = []
    self.high_list = []
    self.low_list = []
    self.trend_list = []
    self._num_days = 0

  def calcPSAR(self, high, low):
    if self._num_days >= 3:
      psar = self._calcPSAR()
    else:
      psar = self._initPSARVals(high, low)

    psar = self._updateCurrentVals(psar, high, low)
    self._num_days += 1

    return psar

  def _initPSARVals(self, high, low):
    if len(self.low_price_window) <= 1:
      self.trend = None
      self.extreme_point = high
      return None

    if self.high_price_window[0] < self.high_price_window[1]:
      self.trend = 1
      psar = min(self.low_price_window)
      self.extreme_point = max(self.high_price_window)
    else:
      self.trend = 0
      psar = max(self.high_price_window)
      self.extreme_point = min(self.low_price_window)

    return psar

  def _calcPSAR(self):
    prev_psar = self.psar_list[-1]
    if self.trend == 1: # Up
      psar = prev_psar + self.af * (self.extreme_point - prev_psar)
      psar = min(psar, min(self.low_price_window))
    else:
      psar = prev_psar - self.af * (prev_psar - self.extreme_point)
      psar = max(psar, max(self.high_price_window))

    return psar

  def _updateCurrentVals(self, psar, high, low):
    if self.trend == 1:
      self.high_price_trend.append(high)
    elif self.trend == 0:
      self.low_price_trend.append(low)

    psar = self._trendReversal(psar, high, low)

    self.psar_list.append(psar)
    self.af_list.append(self.af)
    self.ep_list.append(self.extreme_point)
    self.high_list.append(high)
    self.low_list.append(low)
    self.high_price_window.append(high)
    self.low_price_window.append(low)
    self.trend_list.append(self.trend)

    return psar
  def _trendReversal(self, psar, high, low):
    # Checks for reversals
    reversal = False
    if self.trend == 1 and psar > low:
      self.trend = 0
      psar = max(self.high_price_trend)
      self.extreme_point = low
      reversal = True
    elif self.trend == 0 and psar < high:
      self.trend = 1
      psar = min(self.low_price_trend)
      self.extreme_point = high
      reversal = True

    if reversal:
      self.af = self.init_af
      self.high_price_trend.clear()
      self.low_price_trend.clear()
    else:
        if high > self.extreme_point and self.trend == 1:
          self.af = min(self.af + self.af_step, self.max_af)
          self.extreme_point = high
        elif low < self.extreme_point and self.trend == 0:
          self.af = min(self.af + self.af_step, self.max_af)
          self.extreme_point = low

    return psar"""

class Stb:
    def __init__(self, SYMBOL, amount, token, id, binapi_key, binsecret_key, bitapi_key,
               bitsecret_key, gateapi_key, gatesecret_key, kucapi_key, kucsecret_key,
               passphrase, bin_socket, bit_socket, gate_socket, kuk_socket):

            path = Path("./config.env")
            load_dotenv(dotenv_path=path)
            self.SITE_URL = os.getenv('SITE_URL')
            global running,td,killorder,initial
            running=True
            td=True
            initial=requests.get(url=str(self.SITE_URL)+'/user_exchanges/initial')
            initial=initial.json()
            initial=initial.get('initial')
            self.symbol=SYMBOL

            self.amount=amount

            print('started....')
            self.token=token
            self.id=id
            self.binapi_key=binapi_key
            self.binsecret_key=binsecret_key
            self.bitapi_key=bitapi_key
            self.bitsecret_key=bitsecret_key
            self.kucapi_key=kucapi_key
            self.kucsecret_key=kucsecret_key
            self.passphrase=passphrase
            self.gateapi_key=gateapi_key
            self.gatesecret_key=gatesecret_key
            self.bin_socket=bin_socket
            self.bit_socket=bit_socket
            self.gate_socket=gate_socket
            self.kuc_socket=kuk_socket
            self.socket="wss://stream.binance.com:9443/ws/" + self.symbol.lower() + "@kline_1m"
            self.client = Client('ACebgoy9pnpy0CzbI4xGdeUcVXUaRoO5u5PLKYnz1dp8f4bWlNhS1uhqzxx0Nc1f',
                                 'VbeLJgHSMC8LVUNwFHRvff8UyFwMmjp90NWNXobKHrEfY2dcSxyY7cRDR0Po89g9')
            signal = requests.put(url=self.SITE_URL + '/user_exchanges/stopstatus')
            while td:
                signal = requests.get(url=self.SITE_URL + '/user_exchanges/stopstatus')
                signal = signal.json()
                print(signal)
                print(signal.get('message'))
                if signal.get('shut_down') == '1':
                    td = False
                    break
                self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close,
                                        on_error=self.on_error, on_message=self.on_message)
                self.ws.run_forever()



    def on_message(self, ws, message):


        try:
            signal = requests.get(url=self.SITE_URL + '/user_exchanges/stopstatus')
            signal = signal.json()
            print(signal)
            print(signal.get('message'))
            if signal.get('shut_down') == '1':
                td = False
                self.ws.close()
            if signal.get('signal') == '0':
                if initial == '1':
                    td = False
                    self.ws.close()
            self.trade()
            if killorder == 1:
                td = False

        except BinanceAPIException as e:
            print(e)

    def on_open(self,*args):
        print("Connection Opened")
    def on_close(self,*args):
        print('Conection Closed')
    def on_error(self,*args):
        print("Here is an error : ",args)
    def trade(self):

            global running
            #global side
            global initial
            global killorder
            global td
            side=None
            while running:
                signal=requests.get(url=self.SITE_URL+'/user_exchanges/stopstatus')
                signal=signal.json()
                print(signal.get('message'))
                if signal.get('shut_down')=='1':
                    td=False
                    running=False
                    return 0
                if signal.get('signal')=='0':
                    if initial=='1':
                        td=False
                        running=False
                        return 0
                    else:
                        killorder=1
                print('running-->',running)
                print(initial)
                side = self.set_symbol(initial)

                if side == 'buy':
                    initial = '0'
                    initial_ = requests.post(url=self.SITE_URL+'/user_exchanges/initial',data={'initial':'0'})
                    break
                if side == 'sell':
                    initial = '1'
                    initial_ = requests.post(url=self.SITE_URL+'/user_exchanges/initial', data={'initial': '1'})
                    break

           
            obj = second.First(self.symbol)
            data = obj.coin()
            lst = [i[1] for i in data]

            if side is not None:
                self.ws.close()
                if side=='sell':
                
                    API_KEY = 'ACebgoy9pnpy0CzbI4xGdeUcVXUaRoO5u5PLKYnz1dp8f4bWlNhS1uhqzxx0Nc1f'
                    SECRET_KEY = 'VbeLJgHSMC8LVUNwFHRvff8UyFwMmjp90NWNXobKHrEfY2dcSxyY7cRDR0Po89g9'

                    client = Client(api_key=API_KEY, api_secret=SECRET_KEY, )

                    balance = client.get_account()['balances']
                    balance = [i for i in balance if i.get('asset') == 'BTC']
                    price=balance[0].get('free')[:7]
                elif side=='buy':
                    url = "https://api.binance.com/api/v1/ticker/price"

                    data = requests.get(url)

                    data = data.json()

                    a = [int(float(i.get("price"))) for i in data if self.symbol in i.get("symbol")]

                    a = float("".join(map(str, a)))
                    price = round(float(self.amount) / float(a), 5)
                if 'Binance' in lst:
                    t1 = threading.Thread(target=binance_trade,args=(side,price,self.symbol,))
                    t1.start()

                '''if 'Kucoin' in lst:
                    SYMBOL=data[lst.index('Kucoin')][2]
                    t2 = threading.Thread(target=kucoin_trade,
                    args=(SYMBOL,side, self.amount, self.token, self.id, self.kucapi_key, self.kucsecret_key, self.passphrase, self.kuc_socket))
                    t2.start()
                if 'GateIo' in lst:
                    print('hello')
                    price = data[lst.index('GateIo')][0]
                    SYMBOL = data[lst.index('GateIo')][2]
                    t3 = threading.Thread(target=gateio_trade,
                    args=(SYMBOL, side, price, self.amount, self.token, self.id, self.gateapi_key, self.gatesecret_key, self.gate_socket))
                    t3.start()
                    '''



    def getting_data(self):
        # try:
            starttime = '1 week ago UTC'
            interval = '1m'
            bars = self.client.get_historical_klines(
                self.symbol, interval, starttime)
            for line in bars:
                del line[5:]
            data = pd.DataFrame(
                bars, columns=['Date', 'Open', 'High', 'Low', 'Close'])
            data['Open'] = data['Open'].astype(float)
            data['High'] = data['High'].astype(float)
            data['Low'] = data['Low'].astype(float)
            data['Close'] = data['Close'].astype(float)
            data['7sma'] = data['Close'].rolling(7).mean()
            data['25sma'] =data['Close'].rolling(25).mean()
            #sar = PSAR()
            #data['PSAR'] = data.apply(
            #    lambda x: sar.calcPSAR(x['High'], x['Low']), axis=1)
            data['PSAR'] = talib.SAR(data.High, data.Low, acceleration=0.02, maximum=0.2)
    
            return data
        # except:
        #     print('An error occured in During getting data from API')

    def set_symbol(self, last_symbol):
        # try:
            initial = 'buy'
            if last_symbol == '0':
                initial = 'sell'
            df = self.getting_data()
            ma7c = float(df.tail(1)['7sma'])
            ma25c = float(df.tail(1)['25sma'])
            ma7s = float(df.take([-2])['7sma'])
            ma25s = float(df.take([-2])['25sma'])
            closeprice=float(df.tail(1)['Close'])
            lastopen=list(df.tail(2)['Open'])
            sar=list(df.tail(2)['PSAR'])
            print('MA(7)--> ',ma7c,' MA(25)--> ',ma25s,'SAR --> ',sar[1])
            # print('Current Price -->' ,closeprice,' SAR --->',sar[1])
            if initial == 'buy':
                val = ma7c - ma25c
                if (val >= 0.01) and (ma7s < ma25s) :
                # if float(sar[1])<closeprice and float(sar[0])>float(lastopen[0]):
                    return 'buy'
                else:
                    return None
            elif initial == 'sell':
                val = ma7c - ma25c
                #if val < 0.00:
                if (float(sar[1]) >= closeprice) or val <0.00:
                    return 'sell'
                else:
                    return None
            else:
                return None
        # except:
        #     print('An error occured in bot')





