from django.db import models


from datetime import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser
import public_ip as ip

class User(AbstractUser):
    phone_no = models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    email_verified_at = models.CharField(max_length=200)
    role = models.CharField(max_length=30, default='3')
    status = models.CharField(max_length=20, default='1')
    #log_id = models.CharField(max_length=200,default=ip.get())
    updated_at = models.CharField(max_length=200,default=datetime.utcnow())
    created_at = models.CharField(max_length=200)

