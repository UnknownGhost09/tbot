import schedule
import time
import second
import BinanceTradeBot

import threading
import kucoin_
import Gate_io
running=True
class Stb:
    def __init__(self, SYMBOL, amount, token,id,binapi_key,binsecret_key,bitapi_key,bitsecret_key,gateapi_key,gatesecret_key,kucapi_key,kucsecret_key,passphrase,bin_socket,bit_socket,gate_socket,kuk_socket):
        print('hello')
        schedule.every(10).seconds.do(lambda: job(SYMBOL,amount, token,id,binapi_key,binsecret_key,bitapi_key,bitsecret_key,gateapi_key,gatesecret_key,kucapi_key,kucsecret_key,passphrase,bin_socket,bit_socket,gate_socket,kuk_socket))
        while running:
            schedule.run_pending()
            time.sleep(1)


def cancel_job():
    global running
    running=False
    schedule.CancelJob
    print('Job Canceled')


def binance_trade(SYMBOL, mode, limit, amount, token,id,binapi_key,binsecret_key,bin_socket):
    bot = BinanceTradeBot.TradeBot(SYMBOL, mode, limit, amount, token,id,binapi_key,binsecret_key,bin_socket)
    return bot





def kucoin_trade(symbol, side, size, token,id,kucapi_key,kucsecret_key,passphrase,kuk_socket):
    obj = kucoin_.TradeBot(symbol, side, size, token,id,kucapi_key,kucsecret_key,passphrase,kuk_socket)

    return obj


def gateio_trade(symbol, side, price, amount, token,id,gateapi_key,gatesecret_key,gate_socket):
    obj = Gate_io.TradeBot(symbol, side, price, amount, token,id,gateapi_key,gatesecret_key,gate_socket)
    obj.global_()
    return obj


def job(SYMBOL, amount, token,id,binapi_key,binsecret_key,bitapi_api,bitsecret_key,gateapi_key,gatesecret_key,kucapi_key,kucsecret_key,passphrase,bin_socket,bit_socket,gate_socket,kuk_socket):
    data = second.First(SYMBOL)
    data = data.coin()
    print(data)
    if data[0][1] == 'Binance':
        mode = 'BUY'
        limit = float(data[0][0])
        SYMBOL = data[0][2]
        #amount=0.01
        t1 = threading.Thread(target=binance_trade, args=(SYMBOL, mode, limit, amount, token,id,binapi_key,binsecret_key,bin_socket))
    elif data[1][1] == 'Binance':
        mode = 'SELL'
        limit = float(data[1][0])
        SYMBOL = data[1][2]
        #amount=0.01
        t2 = threading.Thread(target=binance_trade, args=(SYMBOL, mode, limit, amount, token,id,binapi_key,binsecret_key,bin_socket))

    if data[0][1] == 'Kucoin':
        symbol = data[0][2]
        side = 'buy'
        #size = 1  # Here i need to set amount in future
        t1 = threading.Thread(target=kucoin_trade, args=(symbol, side, amount, token,id,kucapi_key,kucsecret_key,passphrase,kuk_socket))
    elif data[1][1] == 'Kucoin':
        symbol = data[1][2]
        side = 'sell'
        #size = 1  # Here i need to set amount in future
        t2 = threading.Thread(target=kucoin_trade, args=(symbol, side, amount, token,id,kucapi_key,kucsecret_key,passphrase,kuk_socket))
    if data[0][1] == 'GateIo':
        symbol = data[0][2]
        side = 'buy'
        price = float(data[0][0])
        #amount = 1  # Here i need to set amount in future
        t1 = threading.Thread(target=gateio_trade, args=(symbol, side, price, amount, token,id,gateapi_key,gatesecret_key,gate_socket))
    elif data[1][1] == 'GateIo':
        symbol = data[1][2]
        side = 'sell'
        price = float(data[1][0])
        #amount = 1  # Here i need to set amount in future
        t2 = threading.Thread(target=gateio_trade, args=(symbol, side, price, amount, token,id,gateapi_key,gatesecret_key,gate_socket))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

