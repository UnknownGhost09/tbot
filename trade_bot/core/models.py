from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser
import public_ip as ip
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)
class User(AbstractUser):
    phone_no = models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    email_verified_at = models.CharField(max_length=200)
    role = models.CharField(max_length=30, default='3')
    status = models.CharField(max_length=20, default='1')
    log_id = models.CharField(max_length=200,default=ip.get())
    updated_at = models.CharField(max_length=200,default=datetime.utcnow())
    created_at = models.CharField(max_length=200)

class App_model(models.Model):
    app_name=models.CharField(max_length=200,primary_key=True,db_column='app_name')
    app_des=models.CharField(max_length=1000)
    app_logo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    app_title=models.CharField(max_length=200)
    copyright=models.CharField(max_length=200)