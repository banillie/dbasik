# Generated by Django 2.1.3 on 2018-11-26 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("register", "0008_auto_20181122_1653"),
        ("datamap", "0007_auto_20181116_1552"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReturnItem",
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
                ("value_str", models.CharField(blank=True, default="", max_length=255)),
                ("value_int", models.IntegerField(blank=True)),
                (
                    "value_float",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=9),
                ),
                ("value_date", models.DateTimeField(blank=True)),
                (
                    "datamap",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamap.Datamap",
                    ),
                ),
                (
                    "financial_quarter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="register.FinancialQuarter",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="register.Project",
                    ),
                ),
            ],
        ),
    ]
