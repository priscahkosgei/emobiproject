from django import forms
from healthApp.models import Product, ImageModel, PatientsModel, DoctorsModel, MedicalReportModel, Appointment, Hospital, CustomUser
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = CustomUser
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['full_name', 'county', 'constituency', 'town', 'hospital_type']

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
