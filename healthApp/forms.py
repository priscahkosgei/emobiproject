from django import forms
from healthApp.models import Product, ImageModel, PatientsModel, DoctorsModel, MedicalReport, Appointment, Hospital, CustomUser, Doctor, Patient
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
        # Set initial value for password1
        self.fields['password1'].initial = '@hospital1'
        # Set initial value for password2
        self.fields['password2'].initial = '@hospital1'


    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['full_name', 'county', 'constituency', 'town', 'hospital_type']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['full_name', 'department']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'date_of_birth', 'gender', 'contact', 'county', 'constituency', 'town']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['title', 'content', 'drugs']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'color']



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image', 'title', 'price']


class PatientsModelForm(forms.ModelForm):
    class Meta:
        model = PatientsModel
        fields = ['full_name',
                  'date_of_birth', 'residence', 'id_no']


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
