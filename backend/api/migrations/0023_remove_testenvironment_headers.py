# Generated by Django 4.2 on 2024-04-17 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0022_alter_datasource_env"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="testenvironment",
            name="headers",
        ),
    ]
