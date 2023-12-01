# Generated by Django 4.2.7 on 2023-11-30 17:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0007_alter_medicalreportmodel_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalreportmodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='medicalreportmodel',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 11, 30, 17, 13, 35, 205541)),
        ),
        migrations.AlterField(
            model_name='medicalreportmodel',
            name='report_id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]