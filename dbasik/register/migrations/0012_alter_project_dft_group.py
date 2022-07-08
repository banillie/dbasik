# Generated by Django 4.0.2 on 2022-07-08 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_dftdivision_id_alter_dftgroup_id_and_more'),
        ('register', '0011_alter_project_dft_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dft_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.dftgroup'),
            preserve_default=False,
        ),
    ]
