# Generated by Django 4.0.2 on 2022-02-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("templates", "0004_auto_20190224_2006"),
    ]

    operations = [
        migrations.AlterField(
            model_name="template",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="templatedataline",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
