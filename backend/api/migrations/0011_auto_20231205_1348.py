# Generated by Django 3.0.6 on 2023-12-05 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20231205_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='api',
            name='params',
            field=models.TextField(default=None, verbose_name='Api Params'),
        ),
        migrations.AlterField(
            model_name='api',
            name='raw',
            field=models.TextField(default=None, verbose_name='Api raw'),
        ),
    ]