# Generated by Django 4.0.5 on 2023-03-11 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_exchanges', '0006_botstop_shut_down'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='binance_model',
            table='binance_model',
        ),
        migrations.AlterModelTable(
            name='binancekeys1',
            table='binanace_keys1',
        ),
        migrations.AlterModelTable(
            name='bitmex_model',
            table='bitmex_model',
        ),
        migrations.AlterModelTable(
            name='exception',
            table='exception',
        ),
        migrations.AlterModelTable(
            name='exchanges',
            table='exchanges',
        ),
        migrations.AlterModelTable(
            name='fills',
            table='fills',
        ),
        migrations.AlterModelTable(
            name='gate_model',
            table='gate_model',
        ),
        migrations.AlterModelTable(
            name='gateiokeys1',
            table='gate_keys1',
        ),
        migrations.AlterModelTable(
            name='kucoin_model',
            table='kucoin_model',
        ),
        migrations.AlterModelTable(
            name='kucoinkeys1',
            table='kucoin_keys1',
        ),
        migrations.AlterModelTable(
            name='pairtable',
            table='pair_table',
        ),
    ]