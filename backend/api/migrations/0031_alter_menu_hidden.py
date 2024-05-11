# Generated by Django 5.0.4 on 2024-05-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0030_alter_datastructure_type_menu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="hidden",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Menu Hidden"
            ),
        ),
    ]
