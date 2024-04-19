from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_type, username,  password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        if not user_type:
            raise ValueError('The user type must be set')
        user = self.model(username=username,
                          user_type=user_type, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_type, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, user_type, username, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('hospital', 'Hospital'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin')
    ]
    user_type = models.CharField(('user type'), max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'  # Set email as the unique identifier for authentication
    REQUIRED_FIELDS = ['user_type', 'username']

    objects = CustomUserManager()

    # Add unique related_name for groups and user_permissions fields
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='custom_user_groups',
    #     blank=True,
    #     verbose_name='groups',
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='custom_user_permissions',
    #     blank=True,
    #     verbose_name='user permissions',
    #     help_text='Specific permissions for this user.',
    #     related_query_name='custom_user',
    # )

    def __str__(self):
        return self.email


class Hospital(models.Model):
    """
    Defines Hospital model
    """
    HOSPITAL_TYPE_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public')
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    full_name = models.CharField(max_length=255, unique=True)
    county = models.CharField(max_length=100)
    constituency = models.CharField(max_length=150)
    town = models.CharField(max_length=200)
    hospital_type = models.CharField(
        max_length=100, choices=HOSPITAL_TYPE_CHOICES)


class Doctor(models.Model):
    """
    Defines Doctor model
    """
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('hepatology', 'Hepatology'),
        ('pediatrics', 'Pediatrics'),
        ('neurology', 'Neurology'),
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    image = models.ImageField(upload_to='doctors/')

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='patients/')
    contact = models.CharField(max_length=30)
    county = models.CharField(max_length=100)
    constituency = models.CharField(max_length=150)
    town = models.CharField(max_length=100)

class MedicalReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateField(default=timezone.now())
    title = models.CharField(max_length=255)
    drugs = models.TextField()

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
