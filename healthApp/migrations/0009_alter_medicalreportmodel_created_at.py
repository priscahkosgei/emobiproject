# Generated by Django 4.2.7 on 2023-11-30 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0008_remove_medicalreportmodel_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalreportmodel',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 11, 30, 17, 14, 41, 65182)),
        ),
    ]