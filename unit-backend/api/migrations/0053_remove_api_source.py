# Generated by Django 5.0.4 on 2024-09-25 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0052_alter_closedtasksdetail_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="api",
            name="source",
        ),
    ]