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
        db_table = 'Binance_model'


class Fills(models.Model):
    clientOrderId = models.ForeignKey(Binance_model,on_delete=models.CASCADE,db_column='clientOrderId')
    commission = models.CharField(max_length=200)
    commissionAsset = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    qty = models.CharField(max_length=200)
    tradeId = models.CharField(max_length=200)

    class Meta:
        db_table = 'Fills'

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
        db_table='Exception'


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
        db_table = 'Bitmex_model'


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
        db_table = 'Kucoin_model'


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
        db_table = 'Gate_model'

class Exchanges(models.Model):
    exchange_name=models.CharField(max_length=200,primary_key=True,db_column='exchange_name')
    Symbol=models.CharField(max_length=300)
    api=models.CharField(max_length=300)
    socket = models.CharField(max_length=300,default='dsgdfgsd')
    status = models.CharField(max_length=200,default='1')
    api_key = models.CharField(max_length=300,default='api')
    secret_key = models.CharField(max_length=300,default='secret')
    passphrase = models.CharField(max_length=200,default='1')
    class Meta:
        db_table='Exchanges'

class PairTable(models.Model):
    pair=models.CharField(max_length=200)
    coin=models.CharField(max_length=200)
    class Meta:
        db_table='Pair_Table'

class BinanceKeys(models.Model):
    id=models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key=models.CharField(max_length=500)
    secret_key=models.CharField(max_length=500,primary_key=True)
    class Meta:
        db_table='Binanace_keys'
class BitmexKeys(models.Model):
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key=models.CharField(max_length=500)
    secret_key=models.CharField(max_length=500,primary_key=True)
    class meta:
        db_table='Bitmex_keys'
class KucoinKeys(models.Model):
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key = models.CharField(max_length=500)
    secret_key = models.CharField(max_length=500,primary_key=True)
    passphrase=models.CharField(max_length=200)
    class Meta:
        db_table='Kucoin_keys'
class GateIoKeys(models.Model):
    id = models.ForeignKey('core.User', on_delete=models.CASCADE, db_column='id')
    api_key = models.CharField(max_length=500)
    secret_key = models.CharField(max_length=500,primary_key=True)
    class Meta:
        db_table='Gate_keys'




