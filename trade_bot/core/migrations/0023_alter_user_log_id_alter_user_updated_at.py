# Generated by Django 4.0.5 on 2023-03-16 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='log_id',
            field=models.CharField(default='49.43.101.79', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2023, 3, 16, 6, 41, 39, 647418), max_length=200),
        ),
    ]
