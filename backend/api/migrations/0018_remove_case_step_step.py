# Generated by Django 4.2 on 2023-12-21 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_case'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='step',
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sort', models.CharField(blank=True, max_length=50, null=True, verbose_name='Step Sort')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Step Name')),
                ('method', models.CharField(blank=True, max_length=50, null=True, verbose_name='Step Method')),
                ('url', models.TextField(default=None, verbose_name='Step Url')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Step Desc')),
                ('headers', models.TextField(default=None, verbose_name='Step Headers')),
                ('params', models.TextField(default=None, verbose_name='Step Params')),
                ('raw', models.TextField(default=None, verbose_name='Step raw')),
                ('setup_script', models.TextField(default=None, verbose_name='Step SetupScript')),
                ('teardown_script', models.TextField(default=None, verbose_name='Step TeardownScript')),
                ('validate', models.TextField(default=None, verbose_name='Step Validate')),
                ('extract', models.TextField(default=None, verbose_name='Step Extract')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Step CreateTime')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='Step UpdateTime')),
                ('case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='step', to='api.case', verbose_name='Case')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='step_creator', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Step',
                'verbose_name_plural': 'Step',
            },
        ),
    ]
