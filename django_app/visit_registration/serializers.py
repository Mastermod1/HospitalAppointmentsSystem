from rest_framework import serializers
from .models import Specialization, DoctorProfile, PatientProfile, Appointment, Visit
from django.contrib.auth.models import User


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialization']


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientProfile
        fields = ['id', 'user', 'date_of_birth']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    patient = PatientProfileSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'doctor', 'patient', 'status', 'place']


class VisitSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()
    patient = PatientProfileSerializer()
    appointment = AppointmentSerializer()

    class Meta:
        model = Visit
        fields = ['id', 'doctor', 'patient', 'appointment', 'interview', 'recommendations']
        extra_kwargs = {
            'interview': {'help_text': 'Ww'},
            'recommendations': {'help_text': 'Lol'},
        }
