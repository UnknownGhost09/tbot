import BinanceTradeBot
import threading
import kucoin_
import Gate_io
from binance.client import Client
import pandas as pd
import requests
import second
import os
from dotenv import load_dotenv
from pathlib import Path
running = True
td = True
killorder=0

def binance_trade(SYMBOL,side, amount, token, id, binapi_key, binsecret_key, bin_socket):
    bot = BinanceTradeBot.TradeBot(SYMBOL, side, amount, token, id, binapi_key, binsecret_key, bin_socket)
    return bot

def kucoin_trade(symbol, side, amount, token, id, kucapi_key, kucsecret_key, passphrase, kuk_socket):
    obj = kucoin_.TradeBot(symbol, side, amount, token, id, kucapi_key, kucsecret_key, passphrase, kuk_socket)
    return obj

def gateio_trade(symbol, side, price, amount, token, id, gateapi_key, gatesecret_key, gate_socket):
    obj = Gate_io.TradeBot(symbol, side, price, amount, token, id, gateapi_key, gatesecret_key, gate_socket)
    print(obj)
    return obj
class Stb:
    def __init__(self, SYMBOL, amount, token, id, binapi_key, binsecret_key, bitapi_key,
               bitsecret_key, gateapi_key, gatesecret_key, kucapi_key, kucsecret_key,
               passphrase, bin_socket, bit_socket, gate_socket, kuk_socket):

        try:
            path = Path("./config.env")
            load_dotenv(dotenv_path=path)
            self.SITE_URL = os.getenv('SITE_URL')
            global running
            global td
            global killorder
            global initial
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
            self.client = Client('7gr7eBfTq9IqaexFkjRVje17t8dTLjE30fck2oVucTURRqOqlYULW8xnKh8rMiZR',
                                 'Ai6F7MpVZvHQBHC0Yb07Djs5I2bmjUqsRVgssjPn3UzcviVn8VbSg5L3ZiC3pYjM')
            signal = requests.put(url=self.SITE_URL+'/user_exchanges/stopstatus')
            while td:
                signal = requests.get(url=self.SITE_URL+'/user_exchanges/stopstatus')
                signal = signal.json()
                print(signal)
                print(signal.get('message'))
                if signal.get('shut_down')=='1':
                    td=False
                    break
                if signal.get('signal') == '0': # initially there is message
                    if initial == '1':
                        td = False
                        break
                self.trade()
                if killorder==1:
                    td=False
        except:
            print('An error occured')
    def trade(self):
        try:
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

            url = "https://api.binance.com/api/v1/ticker/price"
            data = requests.get(url)
            data = data.json()
            a = [int(float(i.get("price"))) for i in data if self.symbol in i.get("symbol")]
            a = float("".join(map(str, a)))
            self.amount = round(self.amount/a,5)
            obj = second.First(self.symbol)
            data = obj.coin()
            lst = [i[1] for i in data]

            if side is not None:
                if 'Binance' in lst:
                    t1 = threading.Thread(target=binance_trade,
                                          args=(self.symbol, side,
                                                self.amount, self.token,
                                                self.id, self.binapi_key,
                                                self.binsecret_key,
                                                self.bin_socket))
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
                    t3.start()'''

        except:
            print('an error occured in bot')

    def getting_data(self):
        try:
            starttime = '1 week ago UTC'
            interval = '1m'
            bars = self.client.get_historical_klines(
                'BTCUSDT', interval, starttime)
            for line in bars:
                del line[5:]
            df = pd.DataFrame(
                bars, columns=['date', 'open', 'high', 'low', 'close'])
            df['7sma'] = df['close'].rolling(5).mean()
            df['25sma'] = df['close'].rolling(15).mean()
            return df
        except:
            print('An error occured in Bot')

    def set_symbol(self, last_symbol):
        try:
            initial = 'buy'
            if last_symbol == '0':
                initial = 'sell'
            df = self.getting_data()
            ma7c = float(df.tail(1)['7sma'])
            ma25c = float(df.tail(1)['25sma'])
            ma7s = float(df.take([-2])['7sma'])
            ma25s = float(df.take([-2])['25sma'])
            print('MA(5)--> ',ma7s,' MA(15)--> ',ma25s)
            if initial == 'buy':
                val = ma7c - ma25c
                if (val >= 0.01) and (ma7s < ma25s):
                    return 'buy'
                else:
                    return None
            elif initial == 'sell':
                val = ma7c - ma25c
                if val < 0.00:
                    return 'sell'
                else:
                    return None
            else:
                return None
        except:
            print('An error occured in bot')





