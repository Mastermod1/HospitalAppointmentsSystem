from rest_framework import serializers
from .models import Specialization, DoctorProfile, Appointment
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


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'doctor']
