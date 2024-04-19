# Generated by Django 4.2.7 on 2024-04-19 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthApp', '0008_hospital_user_alter_medicalreport_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('hospital', 'Hospital'), ('doctor', 'Doctor'), ('patient', 'Patient'), ('admin', 'Admin')], max_length=20, verbose_name='user type'),
        ),
        migrations.AlterField(
            model_name='medicalreport',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 4, 19, 19, 57, 27, 2684, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='medicalreportmodel',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 4, 19, 12, 57, 27, 2684)),
        ),
    ]
