# Generated by Django 4.1.4 on 2023-02-04 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "user_exchanges",
            "0003_exchanges_socket_exchanges_status_kucoinkeys_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="bitmexkeys",
            old_name="secrets_key",
            new_name="secret_key",
        ),
        migrations.RenameField(
            model_name="gateiokeys",
            old_name="secrets_key",
            new_name="secret_key",
        ),
        migrations.RenameField(
            model_name="kucoinkeys",
            old_name="secrets_key",
            new_name="secret_key",
        ),
    ]
