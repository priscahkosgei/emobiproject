import base64
import json

from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth
from django.http import Http404

from healthApp.models import Member, Product, ImageModel, MedicalReportModel, DoctorsModel, PatientsModel, Hospital
from healthApp.forms import ProductForm, ImageUploadForm, MedicalReportForm, DoctorForm, PatientsModelForm, AppointmentForm, HospitalForm, CustomUserCreationForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, hospital_required

import requests


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(f"User: {user.__dict__}")
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form, 'error': "Invalid credentials"})

    elif request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_user(request):
    """
    Logout view.
    """
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

# Hospital views
@login_required
@hospital_required
def hospital_dashboard(request):
    return render(request, 'hospitals/index.html')

@login_required
@hospital_required
def add_doctor(request):
    if request.method == "POST":
        return redirect('add_doctor')
    else:
        form = DoctorForm()
        return render(request, 'hospitals/add_doctor.html', {'form': form})


# Create your views here.
@login_required
@admin_required
def create_hospital(request):
    """
    Register a new hospital
    """
    current_user = request.user
    print(current_user)
    if request.method == 'POST':
        hospital_form = HospitalForm(request.POST)
        print(request.POST)
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
        print(user_form.errors)
    else:
        hospital_form = HospitalForm()
        user_form = CustomUserCreationForm()

    hospitals = Hospital.objects.all()
    print(hospitals[1].__dict__)
    return render(request, 'create_hospital.html', {'hospital_form': hospital_form, 'user_form': user_form, 'hospitals_list': hospitals})



def register(request):
    if request.method == 'POST':
        member = Member(fullname=request.POST['fullname'], username=request.POST['username'],
                        email=request.POST['email'], password=request.POST['password'])
        member.save()
        return redirect('/')
    else:
        return render(request, 'register.html')


def medical_report(request):
    if request.method == 'POST':
        report = MedicalReportForm(request.POST)
        if report.is_valid():
            report.save()
            return redirect('medical-report')
    else:
        report = MedicalReportForm()
        reports = MedicalReportModel.objects.all()
        return render(request, 'MedicalReport.html', {'report': report, "medical_reports": reports})


def departments(request):
    return render(request, 'departments.html')




def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')

# def doctors(request):
#    return render(request, 'doctors.html')


def doctors(request):
    if request.method == 'POST':
        form = DoctorsModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctors')
        else:
            # errors = form.errors
            # return render(request, 'doctors.html', {'form': form, 'errors': errors})
            patients_form = PatientsModelForm(request.POST)
            if patients_form.is_valid():
                patients_form.save()
                return redirect('doctors')
            else:
                errors = patients_form.errors
                return render(request, 'doctors.html', {'form': patients_form, 'errors': errors})
    else:
        doctor_form = DoctorsModelForm()
        patients_form = PatientsModelForm()
        patients_list = PatientsModel.objects.all()
        doctors_list = DoctorsModel.objects.all()
        return render(request, 'doctors.html', {'doctors_form': doctor_form, 'doctors': doctors_list, 'patient_form': patients_form, 'patients': patients_list})


def view_report(request, report_id):
    try:
        report = get_object_or_404(MedicalReportModel, report_id=report_id)
    except Http404:
        return redirect('medical-report')

    return render(request, 'viewReport.html', {"report": report})


def contact(request):
    return render(request, 'contact.html')


def departments(request):
    return render(request, 'departments.html')


def index(request):
    return render(request, 'index.html')

def appointment_form(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a confirmation page
            return redirect('appointment_confirmation')
    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form})


def add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = ProductForm()
        return render(request, "add.html", {'form': form})


def show(request):
    products = Product.objects.all()
    return render(request, 'show.html', {'products': products})


def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('/show')


def edit(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'edit.html', {'product': product})


def update(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html', {'product': product})


def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Apen Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/showimage')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})


def show_image(request):
    images = ImageModel.objects.all()
    return render(request, 'show_image.html', {'images': images})


def imagedelete(request, id):
    image = ImageModel.objects.get(id=id)
    image.delete()
    return redirect('/showimage')
