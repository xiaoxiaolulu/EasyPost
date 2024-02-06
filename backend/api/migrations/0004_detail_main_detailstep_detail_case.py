# Generated by Django 4.2 on 2024-02-06 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_plan_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Detail",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Detail Name"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Detail State",
                    ),
                ),
                (
                    "all",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Detail All"
                    ),
                ),
                (
                    "success",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Detail Success",
                    ),
                ),
                (
                    "error",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Detail Error",
                    ),
                ),
                (
                    "fail",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Detail Fail"
                    ),
                ),
            ],
            options={
                "verbose_name": "Detail",
                "verbose_name_plural": "Detail",
            },
        ),
        migrations.CreateModel(
            name="Main",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Main Name"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Main State"
                    ),
                ),
                (
                    "all",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Main All"
                    ),
                ),
                (
                    "success",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Main Success",
                    ),
                ),
                (
                    "error",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Main Error"
                    ),
                ),
                (
                    "fail",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Main Fail"
                    ),
                ),
                (
                    "runtime",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Main Runtime",
                    ),
                ),
                (
                    "begin_time",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Main BeginTime",
                    ),
                ),
                (
                    "argtime",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Main Argtime",
                    ),
                ),
                (
                    "pass_rate",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Main PassRate",
                    ),
                ),
                (
                    "tester",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Main Tester"
                    ),
                ),
            ],
            options={
                "verbose_name": "Main",
                "verbose_name_plural": "Main",
            },
        ),
        migrations.CreateModel(
            name="DetailStep",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DetailStep Name",
                    ),
                ),
                (
                    "log_data",
                    models.TextField(default=None, verbose_name="DetailStep LogData"),
                ),
                (
                    "url",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DetailStep Url",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DetailStep Method",
                    ),
                ),
                (
                    "status_code",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DetailStep StatusCode",
                    ),
                ),
                (
                    "response_header",
                    models.TextField(
                        default=None, verbose_name="DetailStep ResponseHeader"
                    ),
                ),
                (
                    "requests_header",
                    models.TextField(
                        default=None, verbose_name="DetailStep RequestHeader"
                    ),
                ),
                (
                    "response_body",
                    models.TextField(
                        default=None, verbose_name="DetailStep ResponseBody"
                    ),
                ),
                (
                    "requests_body",
                    models.TextField(
                        default=None, verbose_name="DetailStep RequestBody"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DetailStep State",
                    ),
                ),
                (
                    "run_time",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="DetailStep RunTime",
                    ),
                ),
                (
                    "validate_extractor",
                    models.TextField(
                        default=None, verbose_name="DetailStep ValidateExtractor"
                    ),
                ),
                (
                    "extras",
                    models.TextField(default=None, verbose_name="DetailStep Extras"),
                ),
                (
                    "case",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="detail_step",
                        to="api.detail",
                        verbose_name="DetailStep Step",
                    ),
                ),
            ],
            options={
                "verbose_name": "DetailStep",
                "verbose_name_plural": "DetailStep",
            },
        ),
        migrations.AddField(
            model_name="detail",
            name="case",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="report_detail",
                to="api.main",
                verbose_name="Detail Response",
            ),
        ),
    ]
