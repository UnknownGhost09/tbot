from rest_framework import serializers
from .models import Binance_model,Bitmex_model,Kucoin_model,Gate_model,Exception,Fills
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

