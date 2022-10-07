# Generated by Django 2.1.3 on 2018-11-26 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("datamap", "0007_auto_20181116_1552"),
        ("returns", "0002_auto_20181126_1629"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="returnitem",
            name="datamap",
        ),
        migrations.AddField(
            model_name="returnitem",
            name="datamapline",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="datamap.DatamapLine",
            ),
        ),
    ]
