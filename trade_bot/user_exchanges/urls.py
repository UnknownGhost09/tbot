
from django.urls import path,include
from . import views

urlpatterns = [
    path("bin",views.Binance_api.as_view()),
    path('bit',views.Bitmex_api.as_view()),
    path('gate',views.Gate_api.as_view()),
    path('kuk',views.Kucoin_api.as_view()),
    path('fills',views.Fills_api.as_view()),
    path('fills/<str:pk>/',views.Fills_api.as_view()),
    path('bot',views.Bot_api.as_view()),
    path('config', views.ConfigApi.as_view()),
    path('set_exchange', views.Set_Exchanges.as_view()),
    path('pairapi', views.PairApi.as_view()),
    path('setbin', views.SetBinanceKeys.as_view(), name='setting secret and primary keys'),
    path('setbit', views.SetBitmexKeys.as_view(), name='setting secret and primary keys'),
    path('setkuc', views.SetKucoinKeys.as_view(), name='setting secret and primary keys'),
    path('setgateio', views.SetGateKeys.as_view(), name='setting secret and primary keys'),
    path('exception',views.ExceptionAPI.as_view(),name='exceptions'),
    path('balance',views.Balance.as_view(),name='getting balance'),
    path('stopstatus',views.StopStatus.as_view(),name='stop status'),
    path('runstatus',views.RunStatus.as_view(),name='running stauts of Bot'),
    path('initial',views.InitialStatus.as_view(),name='initial status of Bot'),
    path('logs',views.LogsApi.as_view(),name='logs')

]