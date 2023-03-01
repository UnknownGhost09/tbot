import BinanceTradeBot
import threading
import kucoin_
import Gate_io
from binance.client import Client
import pandas as pd
import requests
import second
running = True
td = True
killorder=0
initial = 1
def binance_trade(SYMBOL, side, amount, token, id, binapi_key, binsecret_key, bin_socket):
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
        global running
        global td
        global initial
        global killorder
        running=True
        td=True
        self.symbol=SYMBOL
        self.amount=amount
        print(amount)
        self.token=token
        self.id=id
        print('id-->',self.id)
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
        self.client = Client(self.binapi_key, self.binsecret_key)
        signal = requests.patch(url='http://192.168.18.110:8000/user_exchanges/stopstatus')

        while td:
            print('started')
            signal = requests.get(url='http://192.168.18.110:8000/user_exchanges/stopstatus')
            signal = signal.json()
            print('hello')
            print(signal)
            print(signal.get('message'))
            if signal.get('message') == '0':
                if initial == 1:
                    td = False
                    break
            self.trade()
            if killorder==1:
                td=False
    def trade(self):
        global running
        global initial
        global side
        global killorder
        side=None
        while running:
            signal=requests.get(url='http://192.168.18.110:8000/user_exchanges/stopstatus')
            signal=signal.json()
            print(signal.get('message'))
            if signal.get('message')=='0':

                if initial==1:
                    print('BYE')
                    return 0
                else:
                    killorder=1

            print('running-->',running)
            print(initial)
            signal = self.set_symbol(initial)
            print(signal)
            if signal == 'buy':
                initial = 0
                break
            if signal == 'sell':
                initial = 1
                break
        if signal == 'buy':
            side = 'buy'
        elif signal == 'sell':
            side = 'sell'
        obj = second.First(self.symbol)
        data = obj.coin()
        lst = [i[1] for i in data]
        print(data)
        print(lst)
        if side is not None:
            if 'Binance' in lst:
                t1 = threading.Thread(target=binance_trade,
                                      args=(self.symbol, side, self.amount, self.token, self.id, self.binapi_key, self.binsecret_key, self.bin_socket))
                t1.start()
            if 'Kucoin' in lst:
                SYMBOL=data[lst.index('Kucoin')][2]
                t2 = threading.Thread(target=kucoin_trade,
                args=(SYMBOL, side, self.amount, self.token, self.id, self.kucapi_key, self.kucsecret_key, self.passphrase, self.kuc_socket))
                t2.start()
            if 'GateIo' in lst:
                print('hello')
                price = data[lst.index('GateIo')][0]
                SYMBOL = data[lst.index('GateIo')][2]
                t3 = threading.Thread(target=gateio_trade,
                args=(SYMBOL, side, price, self.amount, self.token, self.id, self.gateapi_key, self.gatesecret_key, self.gate_socket))
                t3.start()
        else:
            return 0

    def getting_data(self):
        starttime = '1 week ago UTC'
        interval = '1m'
        bars = self.client.get_historical_klines(
            'BTCUSDT', interval, starttime)
        for line in bars:
            del line[5:]
        df = pd.DataFrame(
            bars, columns=['date', 'open', 'high', 'low', 'close'])
        df['7sma'] = df['close'].rolling(7).mean()
        df['25sma'] = df['close'].rolling(25).mean()
        return df

    def set_symbol(self, last_symbol):
        initial = 'buy'
        if last_symbol == 0:
            initial = 'sell'
        df = self.getting_data()
        ma7c = float(df.tail(1)['7sma'])
        ma25c = float(df.tail(1)['25sma'])
        ma7s = float(df.take([-2])['7sma'])
        ma25s = float(df.take([-2])['25sma'])
        if initial == 'buy':
            val = ma7c - ma25c
            if (val >= 0.01) and (ma7s < ma25s):
                return 'buy'
            else:
                return None
        elif initial == 'sell':
            val = ma7c - ma25c
            if (val <= 0.01) & (ma7s > ma25s):
                return 'sell'
            else:
                return None
        else:
            return None


