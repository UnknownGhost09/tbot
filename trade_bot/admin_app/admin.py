from django.contrib import admin
from .models import EmailModel,SmsModel,App_model
# Register your models here.
admin.site.register(EmailModel)
admin.site.register(SmsModel)
admin.site.register(App_model)
