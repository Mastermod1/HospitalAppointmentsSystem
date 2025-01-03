from django.urls import path
from . import views
from . import rest_interface_views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('api/token/', rest_interface_views.ObtainAuthToken.as_view(), name='token_auth'),
    path('api/get_visits/', rest_interface_views.VisitsEndpoint.as_view(), name='visits'),
    path('api/specializations/', rest_interface_views.SpecializationsEndpoint.as_view(), name='specializations'),
    path('api/doctors/<int:specialization_id>/', rest_interface_views.DoctorEndpoint.as_view(), name='doctors'),
    path('api/doctor_availability/<int:doctor_id>/<str:date>/', rest_interface_views.DoctorAvailabilityEndpoint.as_view(), name='doctor-availability'),
    path('api/make_appointment/', rest_interface_views.AppointmentEndpoint.as_view(), name='doctor-availability'),
]
