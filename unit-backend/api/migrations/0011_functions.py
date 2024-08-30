# Generated by Django 4.2 on 2024-04-02 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_remove_datasource_name_alter_datasource_database"),
    ]

    operations = [
        migrations.CreateModel(
            name="Functions",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Functions Name",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        blank=True, null=True, verbose_name="Functions Content"
                    ),
                ),
                (
                    "remarks",
                    models.TextField(
                        blank=True, null=True, verbose_name="Functions Remarks"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Functions CreateTime"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Functions UpdateTime"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="functions_creator",
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