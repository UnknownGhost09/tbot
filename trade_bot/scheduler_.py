import schedule
import time
import second
import BinanceTradeBot
import bit
import threading
import kucoin_
import Gate_io
class Stb:
    def __init__(self, SYMBOL, amount, token,id):
        self.SYMBOL = SYMBOL
        self.amount = amount
        self.token = token
        self.id=id
        schedule.every(10).seconds.do(lambda: job(self.SYMBOL, self.amount, self.token,self.id))
        while True:
            # Checks whether a scheduled task
            # is pending to run or not
            schedule.run_pending()
            time.sleep(1)


def binance_trade(SYMBOL, mode, limit, amount, token,id):
    bot = BinanceTradeBot.TradeBot(SYMBOL, mode, limit, amount, token,id)
    result = bot.Binance()
    return result


def bitmex_trade(sy, price, order, token,id):
    obj = bit.Tradebot(sy, price, order, token,id)
    result = obj.bitmex_()
    return result


def kucoin_trade(symbol, side, size, token,id):
    obj = kucoin_.TradeBot(symbol, side, size, token,id)
    result = obj.kucoin_()
    return result


def gateio_trade(symbol, side, price, amount, token,id):
    obj = Gate_io.TradeBot(symbol, side, price, amount, token,id)
    result = obj.gateio_()
    return result


def job(SYMBOL, amount, token,id):
    data = second.First(SYMBOL)
    data = data.coin()
    print(data)
    if data[0][1] == 'Binance':
        mode = 'BUY'
        limit = float(data[0][0])
        SYMBOL = data[0][2]
        t1 = threading.Thread(target=binance_trade, args=(SYMBOL, mode, limit, amount, token,id))
    elif data[1][1] == 'Binance':
        mode = 'SELL'
        limit = float(data[1][0])
        SYMBOL = data[1][2]
        t2 = threading.Thread(target=binance_trade, args=(SYMBOL, mode, limit, amount, token,id))
    if data[0][1] == 'Bitmex':
        order = 1000  # Here i need to set amount in future
        price = float(data[0][0])
        sy = data[0][2]
        t1 = threading.Thread(target=bitmex_trade, args=(sy, price, order, token,id))
    elif data[1][1] == 'Bitmex':
        order = -1000  # Here i need to set amount in future
        price = float(data[1][0])
        sy = data[1][2]
        t2 = threading.Thread(target=bitmex_trade, args=(sy, price, order, token,id))
    if data[0][1] == 'Kucoin':
        symbol = data[0][2]
        side = 'buy'
        size = 1  # Here i need to set amount in future
        t1 = threading.Thread(target=kucoin_trade, args=(symbol, side, size, token,id))
    elif data[1][1] == 'Kucoin':
        symbol = data[1][2]
        side = 'sell'
        size = 1  # Here i need to set amount in future
        t2 = threading.Thread(target=kucoin_trade, args=(symbol, side, size, token,id))
    if data[0][1] == 'GateIo':
        symbol = data[0][2]
        side = 'buy'
        price = float(data[0][0])
        amount = 1  # Here i need to set amount in future
        t1 = threading.Thread(target=gateio_trade, args=(symbol, side, price, amount, token,id))
    elif data[1][1] == 'GateIo':
        symbol = data[1][2]
        side = 'sell'
        price = float(data[1][0])
        amount = 1  # Here i need to set amount in future
        t2 = threading.Thread(target=gateio_trade, args=(symbol, side, price, amount, token,id))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

