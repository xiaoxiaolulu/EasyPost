# Generated by Django 5.0.4 on 2024-05-20 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0038_alter_apschedulerjobs_options"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="apschedulerjobs",
            table="apscheduler_jobs",
        ),
    ]