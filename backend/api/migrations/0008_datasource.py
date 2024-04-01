# Generated by Django 4.2 on 2024-04-01 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_detailstep_sort"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataSource",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DataSource Name",
                    ),
                ),
                (
                    "host",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="DataSource Host",
                    ),
                ),
                (
                    "port",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="DataSource Host",
                    ),
                ),
                (
                    "user",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="DataSource Host",
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="DataSource Host",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="DataSource CreateTime"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, verbose_name="DataSource UpdateTime"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="data_source",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "DataSource",
                "verbose_name_plural": "DataSource",
                "ordering": ("-create_time",),
            },
        ),
    ]