# Generated by Django 4.1.7 on 2023-03-27 04:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="address",
        ),
    ]