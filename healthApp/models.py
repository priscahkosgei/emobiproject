from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.


class Member(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.fullname


class Product(models.Model):
    name = models.CharField(max_length=25)
    price = models.IntegerField(default=0)
    description = models.TextField()
    color = models.CharField(max_length=30, default="white")

    def __str__(self):
        return self.name


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=50)
    price = models.CharField(max_length=50)


class MedicalReportModel(models.Model):
    report_id = models.IntegerField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200, null=True)
    created_at = models.DateField(default=datetime.now())
    patient_id = models.ForeignKey("PatientsModel", on_delete=models.CASCADE,)
    doctors_id = models.ForeignKey("DoctorsModel", on_delete=models.CASCADE,)
    report = models.TextField(null=True, default="")

    def __str__(self):
        return self.report_id


class PatientsModel(models.Model):
    patient_id = models.CharField(
        max_length=7, default="", unique=True, blank=True, primary_key=True)
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    residence = models.CharField(max_length=100)
    id_no = models.IntegerField(unique=True, default=0)

    def __str__(self):
        return self.full_name

# Signal to generate unique patient_id before saving the object


@receiver(pre_save, sender=PatientsModel)
def generate_patient_id(sender, instance, **kwargs):
    if not instance.patient_id:
        last_patient = PatientsModel.objects.order_by('patient_id').last()
        new_patient_id = 1 if not last_patient else int(
            last_patient.patient_id[3:]) + 1
        instance.patient_id = f'PAT{new_patient_id:04}'

# Signal to convert patient_id to uppercase before saving


@receiver(pre_save, sender=PatientsModel)
def uppercase_patient_id(sender, instance, **kwargs):
    instance.patient_id = instance.patient_id.upper()


class DoctorsModel(models.Model):
    doctors_id = models.CharField(
        primary_key=True, null=False, max_length=6, unique=True, blank=True)
    fullname = models.CharField(max_length=100)
    id_no = models.IntegerField(unique=True)

    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('hepatology', 'Hepatology'),
        ('pediatrics', 'Pediatrics'),
        ('neurology', 'Neurology'),
        # Add more choices as needed
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    image = models.ImageField(upload_to='doctors/')

    def __str__(self):
        return self.fullname

# Correct indentation for the signal and __str__ method


@receiver(pre_save, sender=DoctorsModel)
def generate_doctors_id(sender, instance, **kwargs):
    if not instance.doctors_id:
        last_doctor = DoctorsModel.objects.order_by('doctors_id').last()
        new_doctor_id = 1 if not last_doctor else int(
            last_doctor.doctors_id[3:]) + 1
        instance.doctors_id = f'DOC{new_doctor_id:03}'

# Convert doctors_id to uppercase
# Signal to convert patient_id to uppercase before saving


@receiver(pre_save, sender=DoctorsModel)
def uppercase_doctors_id(sender, instance, **kwargs):
    instance.doctors_id = instance.doctors_id.upper()

    # models.py
    from django.db import models


class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_for_visit = models.TextField()

    def __str__(self):
        return f"{self.patient_name} - {self.appointment_date} {self.appointment_time}"
