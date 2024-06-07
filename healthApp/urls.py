from django.contrib import admin
from django.urls import path

from EmobilisHealthSystem import settings
from healthApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('view/dashboard', views.view_dashboard, name='view_dashboard'),
    path('accounts/login/', views.login_user, name='login'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('logout/', views.logout_user, name='logout'),

    path('hospitals/new', views.create_hospital, name='create_hospital'),
    path('hospitals/<int:hospital_id>/delete/', views.delete_hospital, name='delete_hospital'),

    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hospital/doctors/new/', views.add_doctor, name='add_doctor'),
    path('hospital/doctors/<int:doctor_id>/delete/', views.delete_doctor, name='delete_doctor'),
    path('hospital/patients/', views.hospital_get_patients, name='get_patients'),
    path('hospital/patients/<int:patient_id>/',
         views.doctor_view_patient, name='view_patient'),
    path('hospital/patients/<int:patient_id>/create-report/',
         views.doctor_create_patient_report, name='create_report'),
    path('hospital/patients/<int:patient_id>/delete/',
         views.delete_patient, name='delete_patient'),
    path('hospital/patients/new/', views.hospital_register_patient, name='add_patient'),

    path('user/', views.patient_detail, name='user_dashboard')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
