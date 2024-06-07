from django.shortcuts import render, redirect, reverse
from healthApp.models import Member, Product, ImageModel, MedicalReport, Hospital, Doctor, Patient, CustomUser
from healthApp.forms import MedicalReportForm, DoctorForm, HospitalForm, CustomUserCreationForm, LoginForm, PatientForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, hospital_required
from django.db.models import Q


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import datetime

# Store 2FA code and expiration in session
TWO_FA_EXPIRY_SECONDS = 300  # 5 minutes


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate a random 2FA code
            code = get_random_string(6, allowed_chars='0123456789')
            # Save the code and expiry time in the session
            request.session['2fa_code'] = code
            request.session['2fa_expiry'] = (datetime.datetime.now(
            ) + datetime.timedelta(seconds=TWO_FA_EXPIRY_SECONDS)).strftime('%Y-%m-%d %H:%M:%S')
            request.session['authenticated_user_id'] = user.id

            # Send the code via email
            send_mail(
                'Your 2FA Code',
                f'Your 2FA code is {code}. It is valid for {TWO_FA_EXPIRY_SECONDS//60} minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )

            # Redirect to the 2FA verification page
            return redirect('verify_2fa')

        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form, 'error': "Invalid credentials"})

    elif request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def verify_2fa(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        stored_code = request.session.get('2fa_code')
        expiry_str = request.session.get('2fa_expiry')
        expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')

        # Check if code is correct and not expired
        if stored_code and entered_code == stored_code and datetime.datetime.now() < expiry:
            user_id = request.session.pop('authenticated_user_id', None)
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                login(request, user)
                # Clear 2FA session data
                request.session.pop('2fa_code', None)
                request.session.pop('2fa_expiry', None)
                # Redirect based on user type
                if user.user_type == 'admin':
                    return redirect('create_hospital')
                elif user.user_type in ['hospital', 'doctor']:
                    return redirect('hospital_dashboard')
                elif user.user_type == 'patient':
                    return redirect('user_dashboard')
                return redirect('user_dashboard')

        return render(request, 'verify_2fa.html', {'error': 'Invalid or expired code.'})

    elif request.method == 'GET':
        return render(request, 'verify_2fa.html')


def index(request):

    return render(request, 'index.html')

def logout_user(request):
    """
    Logout view.
    """
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

# Admin Views
# Register Hospital
@login_required
@admin_required
def create_hospital(request):
    """
    Register a new hospital
    """
    if request.method == 'POST':
        hospital_form = HospitalForm(request.POST)
        user_form = CustomUserCreationForm(request.POST)

        if hospital_form.is_valid() and user_form.is_valid():
            # Save user data
            user = user_form.save(commit=False)
            user.user_type = 'hospital'
            user.save()
            # Assuming user_type is a field in your CustomUser model

            # Associate the user with the hospital
            hospital = hospital_form.save(commit=False)
            hospital.user = user
            hospital.save()

            return redirect('create_hospital')
    else:
        hospital_form = HospitalForm()
        user_form = CustomUserCreationForm()

    hospitals = Hospital.objects.all()
    return render(request, 'create_hospital.html', {'hospital_form': hospital_form, 'user_form': user_form, 'hospitals_list': hospitals})

# Hospital delete 
@login_required
@admin_required
def delete_hospital(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    hospital.delete()
    return redirect('create_hospital')


@login_required
@hospital_required
def delete_doctor(request, doctor_id):
    if request.user.user_type == 'doctor':
        return redirect('add_doctor')
    doctor = Doctor.objects.get(id=doctor_id)
    doctor.delete()
    return redirect('add_doctor')

# Hospital delete Patient
@login_required
@hospital_required
def delete_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.delete()
    return redirect('get_patients')

# Hospital views
@login_required
@hospital_required
def hospital_dashboard(request):
    hospital_id = ""
    hospital = None
    if request.user.user_type == 'doctor':
        hospital_id = Doctor.objects.get(user__id=request.user.id).hospital.id
    else:
        hospital_id = Hospital.objects.get(user__id=request.user.id).id
    hospital = Hospital.objects.get(id=hospital_id)
    doctors = Doctor.objects.filter(hospital__id=hospital.id)
    doctors_count = doctors.count()
    patients_count = Patient.objects.all().count()
    return render(request, 'hospitals/index.html', {'hospital': hospital, 'stats': {'doctors': doctors_count, 'patients': patients_count}, 'doctors': doctors})


@login_required
@hospital_required
def add_doctor(request):
    if request.user.user_type == 'doctor':
        return redirect('hospital_dashboard')
    if request.method == "POST":
        doctors_form = DoctorForm(request.POST)
        user_form = CustomUserCreationForm(request.POST)

        if doctors_form.is_valid() and user_form.is_valid():
            # Save user data
            user = user_form.save(commit=False)
            user.user_type = 'doctor'
            user.save()
            doctor = doctors_form.save(commit=False)
            hospital = Hospital.objects.get(user__id=request.user.id)
            doctor.hospital = hospital
            doctor.user = user
            doctor.save()
        return redirect('add_doctor')
    else:
        hospital = Hospital.objects.get(user__id=request.user.id)
        doctors = Doctor.objects.filter(hospital__user__id=request.user.id)
        doctors_form = DoctorForm()
        user_form = CustomUserCreationForm()
        return render(request, 'hospitals/add_doctor.html', {'doctors_form': doctors_form, 'users_form': user_form, 'doctors': doctors, 'hospital': hospital})

@login_required
@hospital_required
def hospital_get_patients(request):
    hospital_id = ""
    hospital = None
    if request.user.user_type == 'doctor':
        hospital_id = Doctor.objects.get(user__id=request.user.id).hospital.id
    else:
        hospital_id = Hospital.objects.get(user__id=request.user.id).id
    hospital = Hospital.objects.get(id=hospital_id)

    if request.method == 'GET':
        hospital = Hospital.objects.get(id=hospital_id)
        query = request.GET.get('q')
        if query:
            # Filter patients based on search query
            patients = Patient.objects.filter(
                Q(full_name__icontains=query) | Q(id__icontains=query)
            )
        else:
            patients = Patient.objects.all()
        return render(request, 'hospitals/patients.html', {'hospital': hospital, 'patients': patients})
# Register Patient
@login_required
@hospital_required
def hospital_register_patient(request):
    hospital_id = ""
    hospital = None
    if request.user.user_type == 'doctor':
        hospital_id = Doctor.objects.get(user__id=request.user.id).hospital.id
    else:
        hospital_id = Hospital.objects.get(user__id=request.user.id).id
    hospital = Hospital.objects.get(id=hospital_id)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES)
        user_form = CustomUserCreationForm(request.POST)

        if patient_form.is_valid() and user_form.is_valid():
            # Save user data
            user = user_form.save(commit=False)
            user.user_type = 'patient'
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('add_patient')
        else:
            print(patient_form.errors)
        return redirect('add_patient')
    elif request.method == 'GET':
        patient_form = PatientForm()
        user_form = CustomUserCreationForm()
        return render(request, 'hospitals/add_patient.html', {'hospital': hospital, 'patient_form': patient_form, 'user_form': user_form})

# Doctor view patients medical history
@login_required
@hospital_required
def doctor_view_patient(request, patient_id):
    if request.user.user_type == 'hospital':
        return redirect('hospital_dashboard')
    doctor = Doctor.objects.get(user__id=request.user.id)
    hospital = Hospital.objects.get(id=doctor.hospital_id)
    if request.method == 'POST':
        return redirect('view_patient')
    else:
        patient = Patient.objects.get(id=patient_id)
        reports = MedicalReport.objects.filter(patient__id=patient.id)
        return render(request, 'hospitals/patient_view.html', {'patient': patient, 'hospital': hospital, 'reports': reports})
    
@login_required
@hospital_required
def doctor_create_patient_report(request, patient_id):
    if request.user.user_type == 'hospital':
        return redirect('hospital_dashboard')
    patient = Patient.objects.get(id=patient_id)
    doctor = Doctor.objects.get(user__id=request.user.id)
    hospital = Hospital.objects.get(id=doctor.hospital_id)
    if request.method == 'POST':
        form = MedicalReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.doctor = doctor
            report.save()
        else:
            print(form.errors)
        url = reverse('create_report', kwargs={'patient_id': patient.id})
        return redirect(url)
    else:
        form = MedicalReportForm()
        return render(request, 'hospitals/create_report.html', {'form': form, 'hospital': hospital, 'patient': patient})

# Patient Views
@login_required
def patient_detail(request):
    patient = Patient.objects.get(user__id=request.user.id)
    medical_reports = MedicalReport.objects.filter(patient__id=patient.id)
    return render(request, 'hospitals/patient_dashboard.html', {'patient': patient, 'reports': medical_reports})


def index(request):
    return render(request, 'index.html')

@login_required
def view_dashboard(request):
    user = request.user
    if user.user_type == 'admin':
        return redirect('create_hospital')
    elif user.user_type == 'hospital' or user.user_type == 'doctor':
        return redirect('hospital_dashboard')
    elif user.user_type == 'patient':
        return redirect('user_dashboard')
    return redirect('user_dashboard')