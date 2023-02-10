from django.db import models
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
# Create your models here.
class EmailModel(models.Model):
    smtp_server = models.CharField(max_length=200)
    mail_from = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    port = models.CharField(max_length=200)
    name = models.CharField(max_length=200,unique=True)
    active_status=models.CharField(max_length=200,default='1')


class SmsModel(models.Model):
    api_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    name = models.CharField(max_length=200,unique=True)
    active_status = models.CharField(max_length=200, default='1')

class App_model(models.Model):
    app_name=models.CharField(max_length=200,unique=True,db_column='app_name')
    app_des=models.CharField(max_length=1000)
    app_logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    app_title=models.CharField(max_length=200)
    copyright=models.CharField(max_length=200)
