from rest_framework import serializers
from .models import EmailModel,SmsModel
from .models import App_model

class Email_serializer(serializers.ModelSerializer):
    class Meta:
        model=EmailModel
        fields='__all__'

class Sms_serializer(serializers.ModelSerializer):

    class Meta:
        model=SmsModel
        fields = '__all__'

class AppSerial(serializers.ModelSerializer):

    class Meta:
        model = App_model
        fields = '__all__'