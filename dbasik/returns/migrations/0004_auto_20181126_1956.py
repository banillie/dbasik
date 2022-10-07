# Generated by Django 2.1.3 on 2018-11-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("returns", "0003_auto_20181126_1636"),
    ]

    operations = [
        migrations.AlterField(
            model_name="returnitem",
            name="value_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="returnitem",
            name="value_float",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=9, null=True
            ),
        ),
        migrations.AlterField(
            model_name="returnitem",
            name="value_int",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
