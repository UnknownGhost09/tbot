from rest_framework import serializers
from .models import Binance_model,Bitmex_model,Kucoin_model,\
    Gate_model,Exception,Fills,Exchanges,PairTable,BinanceKeys,BitmexKeys,GateIoKeys,KucoinKeys
class  BinanceSerial(serializers.ModelSerializer):
    class Meta:
        model=Binance_model
        fields='__all__'


class BitmexSerial(serializers.ModelSerializer):
    class Meta:
        model = Bitmex_model
        fields = '__all__'


class KucoinSerial(serializers.ModelSerializer):
    class Meta:
        model = Kucoin_model
        fields = '__all__'


class GateSerial(serializers.ModelSerializer):
    class Meta:
        model = Gate_model
        fields = '__all__'


class ExceptionSerial(serializers.ModelSerializer):
    class Meta:
        model = Exception
        fields = '__all__'

class Fillserial(serializers.ModelSerializer):
    class Meta:
        model = Fills
        fields = '__all__'

class ExchangesSeial(serializers.ModelSerializer):
    class Meta:
        model = Exchanges
        fields = '__all__'
class PairSerial(serializers.ModelSerializer):
    class Meta:
        model = PairTable
        fields = '__all__'

class GatekeySerial(serializers.ModelSerializer):
    class Meta:
        model= GateIoKeys
        fields='__all__'
class BinanceKeysSerial(serializers.ModelSerializer):
    class Meta:
        model=BinanceKeys
        fields='__all__'
class BitmexKeysSerial(serializers.ModelSerializer):
    class Meta:
        model=BitmexKeys
        fields='__all__'
class KucoinKeysSerial(serializers.ModelSerializer):
    class Meta:
        model=KucoinKeys
        fields='__all__'
