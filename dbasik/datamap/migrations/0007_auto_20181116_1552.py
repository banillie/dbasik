# Generated by Django 2.1.3 on 2018-11-16 15:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datamap", "0006_auto_20180603_1012"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datamapline",
            name="cell_ref",
            field=models.CharField(
                max_length=10,
                validators=[
                    django.core.validators.RegexValidator(
                        message="The cell_ref field must in Excel cell reference format, e.g. 'A10'.",
                        regex="^([A-Z]|[a-z]){1,3}\\d+$",
                    )
                ],
                verbose_name="Cell Reference",
            ),
        ),
    ]
