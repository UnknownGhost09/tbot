# Generated by Django 3.2.18 on 2023-03-13 05:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20230313_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2023, 3, 13, 5, 6, 54, 981078), max_length=200),
        ),
    ]