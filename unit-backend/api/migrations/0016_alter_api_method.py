# Generated by Django 4.2 on 2024-04-10 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_alter_project_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="api",
            name="method",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Api Method"
            ),
        ),
    ]