# Generated by Django 5.1.4 on 2025-01-17 10:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Home", "0008_singer_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="searchquerry",
            name="search",
            field=models.CharField(max_length=500),
        ),
    ]
