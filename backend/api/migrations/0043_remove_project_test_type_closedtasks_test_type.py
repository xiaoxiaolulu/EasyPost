# Generated by Django 5.0.4 on 2024-06-21 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0042_remove_closedtasks_project"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="test_type",
        ),
        migrations.AddField(
            model_name="closedtasks",
            name="test_type",
            field=models.CharField(
                choices=[("UI", "Ui"), ("API", "Api")],
                default="API",
                max_length=50,
                verbose_name="ClosedTasks TestType",
            ),
        ),
    ]
