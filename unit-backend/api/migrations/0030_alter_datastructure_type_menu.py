# Generated by Django 5.0.4 on 2024-05-08 06:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0029_datastructure"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datastructure",
            name="type",
            field=models.CharField(
                choices=[
                    (0, "None"),
                    (1, "Form Data"),
                    (2, "X Www Form Urlencoded"),
                    (3, "Json"),
                ],
                default=0,
                max_length=50,
                verbose_name="DataStructure Type",
            ),
        ),
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Menu Name"
                    ),
                ),
                (
                    "path",
                    models.TextField(blank=True, null=True, verbose_name="Menu Path"),
                ),
                (
                    "component",
                    models.TextField(
                        blank=True, null=True, verbose_name="Menu Component"
                    ),
                ),
                (
                    "redirect",
                    models.TextField(
                        blank=True, null=True, verbose_name="Menu Redirect"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Menu Title"
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Menu Icon"
                    ),
                ),
                (
                    "hidden",
                    models.BooleanField(default=False, verbose_name="Menu Hidden"),
                ),
                (
                    "roles",
                    models.TextField(blank=True, null=True, verbose_name="Menu Roles"),
                ),
                (
                    "parent_id",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Menu ParentId",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Menu CreateTime"
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="Menu UpdateTime"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="menu_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Menu",
                "verbose_name_plural": "Menu",
            },
        ),
    ]