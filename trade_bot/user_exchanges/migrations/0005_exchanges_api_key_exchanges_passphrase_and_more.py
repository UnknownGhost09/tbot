# Generated by Django 4.1.4 on 2023-02-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_exchanges", "0004_rename_secrets_key_bitmexkeys_secret_key_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchanges",
            name="api_key",
            field=models.CharField(default="api", max_length=300),
        ),
        migrations.AddField(
            model_name="exchanges",
            name="passphrase",
            field=models.CharField(default="1", max_length=200),
        ),
        migrations.AddField(
            model_name="exchanges",
            name="secret_key",
            field=models.CharField(default="secret", max_length=300),
        ),
    ]
