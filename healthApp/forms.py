from django import forms
from healthApp.models import Product, ImageModel, PatientsModel, DoctorsModel, MedicalReportModel, Appointment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'color']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = DoctorsModel
        fields = '__all__'


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image', 'title', 'price']


class PatientsModelForm(forms.ModelForm):
    class Meta:
        model = PatientsModel
        fields = ['full_name',
                  'date_of_birth', 'residence', 'id_no']


class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReportModel
        fields = ['title', 'report', 'patient_id', 'doctors_id', 'created_at']


class DoctorsModelForm(forms.ModelForm):
    class Meta:
        model = DoctorsModel
        fields = ['fullname', 'id_no', 'department', 'image']

    department = forms.ChoiceField(choices=DoctorsModel.DEPARTMENT_CHOICES)

    class AppointmentForm(forms.ModelForm):
        class Meta:
            model = Appointment
            fields = ['patient_name', 'contact_number',
                      'appointment_date', 'appointment_time', 'reason_for_visit']


class AppointmentForm:
    pass
