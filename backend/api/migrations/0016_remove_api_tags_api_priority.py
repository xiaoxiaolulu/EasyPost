# Generated by Django 4.2 on 2023-12-21 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_djangoadminaccessipwhitelist_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='tags',
        ),
        migrations.AddField(
            model_name='api',
            name='priority',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0, max_length=50, verbose_name='Api Priority'),
        ),
    ]
