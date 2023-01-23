
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("bin",views.Binance_api.as_view()),
    path('bit',views.Bitmex_api.as_view()),
    path('gate',views.Gate_api.as_view()),
    path('kuk',views.Kucoin_api.as_view()),
    path('fills',views.Fills_api.as_view()),
    path('bot',views.Bot_api.as_view())
]