from django.contrib import admin
from .models import Binance_model,Bitmex_model,Exception,Gate_model,Kucoin_model,Fills,Exchanges,PairTable
# Register your models here.
admin.site.register(Binance_model)
admin.site.register(Bitmex_model)
admin.site.register(Exception)
admin.site.register(Gate_model)
admin.site.register(Kucoin_model)
admin.site.register(Fills)
admin.site.register(Exchanges)
admin.site.register(PairTable)