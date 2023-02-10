from django.contrib import admin
from .models import Binance_model,Bitmex_model,Exception,Gate_model,Kucoin_model,Fills,Exchanges,PairTable,BinanceKeys1,BitmexKeys1,GateIoKeys1,KucoinKeys1
# Register your models here.
admin.site.register(Binance_model)
admin.site.register(Bitmex_model)
admin.site.register(Exception)
admin.site.register(Gate_model)
admin.site.register(Kucoin_model)
admin.site.register(Fills)
admin.site.register(Exchanges)
admin.site.register(PairTable)
admin.site.register(BinanceKeys1)
admin.site.register(GateIoKeys1)
admin.site.register(BitmexKeys1)
admin.site.register(KucoinKeys1)