# Generated by Django 3.0.6 on 2023-11-24 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20230927_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='gateway',
        ),
        migrations.RemoveField(
            model_name='api',
            name='hooks',
        ),
        migrations.AddField(
            model_name='api',
            name='body_type',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default=0, max_length=50, verbose_name='Api BodyType'),
        ),
        migrations.AddField(
            model_name='api',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='Api Desc'),
        ),
        migrations.AddField(
            model_name='api',
            name='setup_script',
            field=models.TextField(default=None, verbose_name='Api SetupScript'),
        ),
        migrations.AddField(
            model_name='api',
            name='status',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2)], default=0, max_length=50, verbose_name='Api Status'),
        ),
        migrations.AddField(
            model_name='api',
            name='tags',
            field=models.TextField(default=None, verbose_name='Api Tags'),
        ),
        migrations.AddField(
            model_name='api',
            name='teardown_script',
            field=models.TextField(default=None, verbose_name='Api TeardownScript'),
        ),
    ]