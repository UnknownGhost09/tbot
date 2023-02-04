from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
 path('',views.user_api.as_view()),
 path('login',views.Login.as_view()),
 path('logout',views.LogOutApi.as_view()),

]