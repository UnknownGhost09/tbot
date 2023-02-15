# Generated by Django 4.1.4 on 2023-02-10 07:10

import admin_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="App_model",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "app_name",
                    models.CharField(db_column="app_name", max_length=200, unique=True),
                ),
                ("app_des", models.CharField(max_length=1000)),
                (
                    "app_logo",
                    models.ImageField(
                        blank=True, null=True, upload_to=admin_app.models.upload_to
                    ),
                ),
                ("app_title", models.CharField(max_length=200)),
                ("copyright", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="EmailModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("smtp_server", models.CharField(max_length=200)),
                ("mail_from", models.CharField(max_length=200)),
                ("username", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=200)),
                ("port", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("active_status", models.CharField(default="1", max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="SmsModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_key", models.CharField(max_length=200)),
                ("secret_key", models.CharField(max_length=200)),
                ("phone_no", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("active_status", models.CharField(default="1", max_length=200)),
            ],
        ),
    ]