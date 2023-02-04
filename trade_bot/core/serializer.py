from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import App_model
User=get_user_model()
class UserSerial(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class AppSerial(serializers.ModelSerializer):
    app_logo = serializers.ImageField(required=False)
    class Meta:
        model = App_model
        fields = '__all__'