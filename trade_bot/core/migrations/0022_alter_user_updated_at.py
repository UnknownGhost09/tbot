# Generated by Django 4.0.5 on 2023-03-13 11:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2023, 3, 13, 11, 2, 10, 583701), max_length=200),
        ),
    ]
