from django.contrib import admin
from django.urls import path

from EmobilisHealthSystem import settings
from healthApp import views
from healthApp.views import appointment_form
from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name= 'register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctorsform/', views.doctorsform, name='doctorsform'),
    path('departments/', views.departments, name='departments'),
    path('appointment/', appointment_form, name='appointment_form'),
    path('contact/', views.contact, name='contact'),
    path('index/', views.index, name='index'),
    path('medical-report/', views.medical_report, name='medical-report'),
    path('departments/', views.departments, name= 'departments'),
    path('add/', views.add, name= 'add'),
    path('show/', views.show, name ='show'),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('uploadimage/', views.upload_image, name='upload'),
    path('showimage/', views.show_image, name='image'),
    path('imagedelete/<int:id>', views.imagedelete),

    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, ocument_root=settings.MEDIA_ROOT)