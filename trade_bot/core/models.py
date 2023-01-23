from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_no = models.CharField(max_length=200)
    email=models.EmailField(unique=True)
    email_verified_at = models.CharField(max_length=200)
    role = models.CharField(max_length=30, default='3')
    status = models.CharField(max_length=20, default='1')
    log_id = models.CharField(max_length=500)
    updated_at = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200)

