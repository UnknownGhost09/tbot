# Generated by Django 4.0.5 on 2023-03-21 11:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_user_log_id_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='log_id',
            field=models.CharField(default='49.43.98.59', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2023, 3, 21, 11, 47, 49, 87367), max_length=200),
        ),
    ]
