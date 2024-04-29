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
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, default=None)
    full_name = models.CharField(max_length=100)
    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('hepatology', 'Hepatology'),
        ('pediatrics', 'Pediatrics'),
        ('neurology', 'Neurology'),
    ]
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    image = models.ImageField(upload_to='doctors/', default="data:image/png;base64,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", null=True)

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, default=None)
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
