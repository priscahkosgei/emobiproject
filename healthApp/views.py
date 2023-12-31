import base64
import json

from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth
from django.http import Http404

from healthApp.models import Member, Product, ImageModel, MedicalReportModel, DoctorsModel, PatientsModel
from healthApp.forms import ProductForm, ImageUploadForm, MedicalReportForm, DoctorsModelForm, DoctorForm, PatientsModelForm, AppointmentForm
from django.http import HttpResponse
from healthApp.credentials import LipanaMpesaPpassword, MpesaAccessToken, MpesaC2bCredential

import requests


# Create your views here.

def doctorsform(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a view displaying the list of doctors
            return redirect('doctor_list')
    else:
        form = DoctorForm()
        return render(request, 'doctorsform.html', {'form': form})


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


def login(request):
    return render(request, 'login.html')


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
    if request.method == 'POST':
        if Member.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
            member = Member.objects.get(
                username=request.POST['username'], password=request.POST['password'])
            return render(request, 'index.html', {'member': member})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


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
