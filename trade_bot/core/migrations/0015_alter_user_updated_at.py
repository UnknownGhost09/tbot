# Generated by Django 4.0.5 on 2023-03-06 05:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_user_log_id_alter_user_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.CharField(default=datetime.datetime(2023, 3, 6, 5, 31, 23, 668843), max_length=200),
        ),
    ]
