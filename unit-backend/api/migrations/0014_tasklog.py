# Generated by Django 4.2 on 2024-04-03 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_address_headers_address_variables"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskLog",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "task_id",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="TaskLog TaskId",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="TaskLog Type",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="TaskLog CreateTime"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, verbose_name="TaskLog UpdateTime"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="taskLog_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "TaskLog",
                "verbose_name_plural": "TaskLog",
            },
        ),
    ]