from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_appointment, name='register'),
    path('success/', views.success, name='success'),
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('patient/dashboard', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard', views.doctor_dashboard, name='doctor_dashboard'),
]
