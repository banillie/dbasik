# Generated by Django 2.1.3 on 2018-11-22 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0006_auto_20181122_1610"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="financialquarter",
            options={"ordering": ["start_date"]},
        ),
        migrations.AlterField(
            model_name="financialquarter",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="financialquarter",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
