# Generated by Django 5.0.4 on 2024-06-21 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0045_alter_closedtasks_test_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="closedtasks",
            name="detail",
        ),
        migrations.CreateModel(
            name="ClosedTasksDetail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "func_name",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="ClosedTasksDetail FuncName",
                    ),
                ),
                (
                    "scene_name",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="ClosedTasksDetail SceneName",
                    ),
                ),
                (
                    "err_step",
                    models.TextField(
                        default="", verbose_name="ClosedTasksDetail ErrStep"
                    ),
                ),
                (
                    "err_type",
                    models.CharField(
                        choices=[
                            ("系统异常", "System Err"),
                            ("用例修正", "Case Err"),
                            ("环境异常", "Environ Err"),
                            ("断言错误", "Assert Err"),
                        ],
                        default="系统异常",
                        max_length=50,
                        verbose_name="ClosedTasksDetail ErrType",
                    ),
                ),
                (
                    "handler",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="ClosedTasksDetail Handler",
                    ),
                ),
                (
                    "cause",
                    models.TextField(
                        default="", verbose_name="ClosedTasksDetail cause"
                    ),
                ),
                (
                    "steps",
                    models.TextField(
                        default=[], verbose_name="ClosedTasksDetail steps"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="task",
                        to="api.closedtasks",
                        verbose_name="ClosedTasksDetail Task",
                    ),
                ),
            ],
            options={
                "verbose_name": "ClosedTasksDetail",
                "verbose_name_plural": "ClosedTasksDetail",
            },
        ),
    ]
