from django import forms
from healthApp.models import Product, ImageModel, PatientsModel, DoctorsModel, MedicalReportModel


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
        fields = ['image','title','price']


class PatientsModelForm(forms.ModelForm):
    class Meta:
        model = PatientsModel
        fields =['patient_id','full_name','date_of_birth','residence','id_no']

class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReportModel
        fields =['report_id', 'created_at', 'report', 'created_at', 'patient_id', 'doctors_id']

class DoctorsModelForm(forms.ModelForm):
    class Meta:
        model = DoctorsModel
        fields = ['fullname', 'id_no', 'department']

    department = forms.ChoiceField(choices=DoctorsModel.DEPARTMENT_CHOICES)