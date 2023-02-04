from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('subadmin_signup',views.SubAdminView.as_view()),
]