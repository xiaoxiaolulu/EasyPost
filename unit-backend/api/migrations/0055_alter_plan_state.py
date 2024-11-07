# Generated by Django 5.0.4 on 2024-11-04 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0054_step_priority_step_status_alter_project_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="state",
            field=models.CharField(
                choices=[(0, "Stop"), (1, "Running")],
                default=1,
                max_length=50,
                verbose_name="Plan State",
            ),
        ),
    ]