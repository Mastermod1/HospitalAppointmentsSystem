from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_appointment, name='register'),
    path('success/', views.success, name='success'),
]
