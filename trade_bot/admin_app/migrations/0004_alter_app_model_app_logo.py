# Generated by Django 4.1.4 on 2023-02-17 11:57

import admin_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_app", "0003_alter_app_model_app_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="app_model",
            name="app_logo",
            field=models.ImageField(
                blank=True, null=True, upload_to=admin_app.models.upload_to
            ),
        ),
    ]
