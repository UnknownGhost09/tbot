from django.db import models



class Binance_model(models.Model):
    id=models.ForeignKey('core.User',on_delete=models.CASCADE,db_column='id')
    clientOrderId = models.CharField(max_length=200,primary_key=True)
    symbol=models.CharField(max_length=200,default='0')
    orderId=models.CharField(max_length=200,default='0')
    OrderListId = models.CharField(max_length=200,default='0')
    executedQty = models.CharField(max_length=200,default='0')
    price = models.CharField(max_length=200,default='0')
    side = models.CharField(max_length=200,default='0')
    status = models.CharField(max_length=200,default='0')
    timeInForce = models.CharField(max_length=200,default='0')
    transactTime = models.CharField(max_length=200,default='0')
    type = models.CharField(max_length=200,default='0')
    workingTime = models.CharField(max_length=200,default='0')

    class Meta:
        db_table = 'binance_model'


class Fills(models.Model):
    clientOrderId = models.ForeignKey(Binance_model,on_delete=models.CASCADE,db_column='clientOrderId')
    commission = models.CharField(max_length=200)
    commissionAsset = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    qty = models.CharField(max_length=200)
    tradeId = models.CharField(max_length=200)

    class Meta:
        db_table = 'fills'

class Exception(models.Model):
    id = models.ForeignKey('core.user',on_delete=models.CASCADE,db_column='id')
    message = models.CharField(max_length=500)
    side = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    #sr = models.IntegerField(primary_key=True)
    sr =  models.AutoField(primary_key=True)
    time = models.CharField(max_length=200)
    Exchange_name = models.CharField(max_length=200)
    status=models.CharField(max_length=100,default=False)
    class Meta:
        db_table='exception'


class Bitmex_model(models.Model):
    id = models.ForeignKey('core.User',on_delete=models.CASCADE,db_column='id')
    orderID = models.CharField(max_length=200,primary_key=True)
    account = models.CharField(max_length=200)
    #clOrdId = models.CharField(max_length=200)
    cumQty = models.CharField(max_length=200)
    currency =  models.CharField(max_length=200)
    ordStatus = models.CharField(max_length=200)
    ordType = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    settlCurrency = models.CharField(max_length=200)
    side = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    timeInForce = models.CharField(max_length=200)
    timestamp = models.CharField(max_length=200)
    transactTime = models.CharField(max_length=200)
    status=models.CharField(max_length=100,default=True)
    class Meta:
        db_table = 'bitmex_model'


class Kucoin_model(models.Model):
    id = models.ForeignKey('core.User',on_delete=models.CASCADE,db_column='id')
    symbol= models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    side = models.CharField(max_length=200)
    orderId = models.CharField(max_length=200,primary_key=True)#OrderId == id
    price = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    timeInforce = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    clientOid = models.CharField(max_length=200)
    class Meta:
        db_table = 'kucoin_model'


class Gate_model(models.Model):
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    symbol = models.CharField(max_length=200)
    currency_pair = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    side = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    time_in_force = models.CharField(max_length=200)
    orderId = models.CharField(max_length=200,primary_key=True)
    status=models.CharField(max_length=200,default=True)
    class Meta:
        db_table = 'gate_model'

class Exchanges(models.Model):
    exchange_name=models.CharField(max_length=200,primary_key=True,db_column='exchange_name')
    Symbol=models.CharField(max_length=300)
    api=models.CharField(max_length=300)
    socket = models.CharField(max_length=300,default='dsgdfgsd')
    status = models.CharField(max_length=200,default='1')
    class Meta:
        db_table='exchanges'

class PairTable(models.Model):
    pair=models.CharField(max_length=200)
    coin=models.CharField(max_length=200)
    class Meta:
        db_table='pair_table'
class BinanceKeys1(models.Model):
    sr =  models.AutoField(primary_key=True)
    id=models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key=models.CharField(max_length=500)
    secret_key=models.CharField(max_length=500)

    class Meta:
        db_table='binanace_keys1'
class BitmexKeys1(models.Model):
    sr =  models.AutoField(primary_key=True)
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key=models.CharField(max_length=500)
    secret_key=models.CharField(max_length=500)
    class meta:
        db_table='bitmex_keys1'
class KucoinKeys1(models.Model):
    sr =  models.AutoField(primary_key=True)
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key = models.CharField(max_length=500)
    secret_key = models.CharField(max_length=500)
    passphrase=models.CharField(max_length=200)
    class Meta:
        db_table='kucoin_keys1'
class GateIoKeys1(models.Model):
    sr =  models.AutoField(primary_key=True)
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key = models.CharField(max_length=500)
    secret_key = models.CharField(max_length=500)
    class Meta:
        db_table='gate_keys1'

class BotStop(models.Model):
    initial=models.CharField(max_length=20,default='1')
    signal=models.CharField(max_length=20,default='0')
    status=models.CharField(max_length=20,default='0')

class KillBot(models.Model):
    shut_down = models.CharField(max_length=20, default='0')

class LogsModel(models.Model):
    sr = models.AutoField(primary_key=True)
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    symbol=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
    side=models.CharField(max_length=200)
    exchange=models.CharField(max_length=200)







