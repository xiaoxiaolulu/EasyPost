# Generated by Django 5.0.4 on 2024-05-17 07:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0034_remove_user_role_userrole"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userrole",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="roles",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]