# Generated by Django 3.2.16 on 2023-01-20 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_exchanges', '0004_bitmex_model_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='gate_model',
            name='status',
            field=models.CharField(default=True, max_length=200),
        ),
    ]
