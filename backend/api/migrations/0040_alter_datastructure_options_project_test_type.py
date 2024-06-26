# Generated by Django 5.0.4 on 2024-06-20 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0039_alter_apschedulerjobs_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="datastructure",
            options={
                "verbose_name": "DataStructure",
                "verbose_name_plural": "DataStructure",
            },
        ),
        migrations.AddField(
            model_name="project",
            name="test_type",
            field=models.CharField(
                choices=[("UI", "Ui"), ("API", "Api")],
                default="API",
                max_length=50,
                verbose_name="Project TestType",
            ),
        ),
    ]
