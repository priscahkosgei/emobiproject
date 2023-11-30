from django.contrib import admin
from healthApp.models import Member, Product, ImageModel,MedicalReportModel,PatientsModel,DoctorsModel

# Register your models here.
admin.site.register(Member)
admin.site.register(Product)
admin.site.register(ImageModel)
admin.site.register(MedicalReportModel)
admin.site.register(PatientsModel)
admin.site.register(DoctorsModel)