from django.contrib import admin
from django.urls import path

from EmobilisHealthSystem import settings
from healthApp import views
from healthApp.views import appointment_form
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accouts/register', views.register, name='register'),
    path('accounts/login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('hospitals/new', views.create_hospital, name='create_hospital'),
    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hospital/doctors/new/', views.add_doctor, name='add_doctor'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
