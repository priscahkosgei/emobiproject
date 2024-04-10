from django.contrib import admin
from healthApp.models import Member, Product, ImageModel,MedicalReportModel,PatientsModel,DoctorsModel, Hospital, Doctor, Patient, MedicalReport, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Member)
admin.site.register(Product)
admin.site.register(ImageModel)
admin.site.register(MedicalReportModel)
admin.site.register(PatientsModel)
admin.site.register(DoctorsModel)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(MedicalReport)
