import second
import BinanceTradeBot
import schedule
import threading
import kucoin_
import Gate_io
import time
class Stb:
    def __init__(self,run ,SYMBOL, amount, token,id,binapi_key,binsecret_key,bitapi_key,bitsecret_key,gateapi_key,gatesecret_key,kucapi_key,kucsecret_key,passphrase,bin_socket,bit_socket,gate_socket,kuk_socket):
        global running
        running=run
        schedule.every(10).seconds.do(lambda: job(SYMBOL,amount, token,id,binapi_key,binsecret_key,bitapi_key,bitsecret_key,gateapi_key,gatesecret_key,kucapi_key,kucsecret_key,passphrase,bin_socket,bit_socket,gate_socket,kuk_socket))
        while running:
            print('all jobs --> ' ,schedule.get_jobs())
            if not schedule.jobs:
                break
            schedule.run_pending()
            time.sleep(1)


def cancel_job():
    global running
    running=False
    schedule.CancelJob
    #schedule.cancel_job(job)
    schedule.clear()
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
    while True:
        data = second.First(SYMBOL)
        data = data.coin()
        if data !=False:
            break
        print('price not found')

    print(data)
    if data[0][1] == 'Binance':
        mode = 'BUY'
        limit = float(data[0][0])
        SYMBOL = data[0][2]
        #amount=0.01

        t1 = threading.Thread(target=binance_trade, args=(SYMBOL, mode, limit, amount, token,id,binapi_key,binsecret_key,bin_socket))
        print('Binance Buy thread created')
    elif data[1][1] == 'Binance':
        mode = 'SELL'
        limit = float(data[1][0])
        SYMBOL = data[1][2]
        #amount=0.01

        t2 = threading.Thread(target=binance_trade, args=(SYMBOL, mode, limit, amount, token,id,binapi_key,binsecret_key,bin_socket))
        print('Binance Sell Thread Created')

    if data[0][1] == 'Kucoin':
        symbol = data[0][2]
        side = 'buy'
        #size = 1  # Here i need to set amount in future
        t1 = threading.Thread(target=kucoin_trade, args=(symbol, side, amount, token,id,kucapi_key,kucsecret_key,passphrase,kuk_socket))
        print('Kucoin Buy thread created')
    elif data[1][1] == 'Kucoin':
        symbol = data[1][2]
        side = 'sell'
        #size = 1  # Here i need to set amount in future
        t2 = threading.Thread(target=kucoin_trade, args=(symbol, side, amount, token,id,kucapi_key,kucsecret_key,passphrase,kuk_socket))
        print('Kucoin sell Thread created')
    if data[0][1] == 'GateIo':
        symbol = data[0][2]
        side = 'buy'
        price = float(data[0][0])
        #amount = 1  # Here i need to set amount in future
        t1 = threading.Thread(target=gateio_trade, args=(symbol, side, price, amount, token,id,gateapi_key,gatesecret_key,gate_socket))
        print('GateIo buy thread created')
    elif data[1][1] == 'GateIo':
        symbol = data[1][2]
        side = 'sell'
        price = float(data[1][0])
        #amount = 1  # Here i need to set amount in future
        t2 = threading.Thread(target=gateio_trade, args=(symbol, side, price, amount, token,id,gateapi_key,gatesecret_key,gate_socket))
        print('GateIo sell Thread Created')

    t1.start()
    t2.start()
    t1.join()
    t2.join()

