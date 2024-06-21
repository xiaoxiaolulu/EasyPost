# Generated by Django 5.0.4 on 2024-06-21 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0044_alter_closedtasks_test_type"),
    ]

    operations = [
        migrations.AlterField(
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
