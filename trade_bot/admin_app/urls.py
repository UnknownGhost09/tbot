from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('subadmin_signup',views.AdminView.as_view()),
    path('user_data',views.UsersData.as_view(),name='length of users'),
    path('app_table', views.AppApi.as_view(), name='setting app data with logo'),
    path('symbol_price', views.PriceAPI.as_view(), name='getting Price of a particular symbol'),
    path('users',views.UsersApi.as_view(),name='Users Detail'),
    path('inact',views.userInactiveApi.as_view(),name='Inactivating user')
]