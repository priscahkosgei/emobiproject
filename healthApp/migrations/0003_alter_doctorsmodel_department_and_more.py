# Generated by Django 4.2.7 on 2023-11-29 20:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0002_alter_medicalreportmodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorsmodel',
            name='department',
            field=models.CharField(choices=[('cardiology', 'Cardiology'), ('hepatology', 'Hepatology'), ('pediatrics', 'Pediatrics'), ('neurology', 'Neurology')], max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalreportmodel',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 11, 29, 12, 8, 43, 74769)),
        ),
    ]
