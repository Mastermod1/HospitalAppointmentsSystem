from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import rest_interface_views

urlpatterns = [
    path('register/', views.register_appointment, name='register'),
    path('success/', views.success, name='success'),
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('api/token/', obtain_auth_token, name='token_auth'),
    path('api/get_visits/', rest_interface_views.VisitsEndpoint.as_view(), name='lol'),
]
