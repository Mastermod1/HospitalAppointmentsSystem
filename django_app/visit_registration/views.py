from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import AppointmentForm
from django.contrib.auth.models import Group, Permission


if not Group.objects.get(name='patient'):
    Group.objects.create(name='patient')
if not Group.objects.get(name='doctor'):
    Group.objects.create(name='doctor')


def is_doctor(user):
    return user.groups.filter(name='doctor').exists()


def is_patient(user):
    return user.groups.filter(name='patient').exists()


@login_required
@user_passes_test(is_doctor)
def doctor_view(request):
    return render(request, 'doctor_dashboard.html')


@login_required
@user_passes_test(is_doctor)
def patient_view(request):
    return render(request, 'patient_dashboard.html')


def register_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AppointmentForm()
    return render(request, 'register.html', {'form': form})


def success(request):
    return render(request, 'success.html')


@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')


class CustomLoginView(LoginView):
    def get_success_url(self):
        if is_doctor(self.request.user):
            return resolve_url('doctor_dashboard')
        if is_patient(self.request.user):
            return resolve_url('patient_dashboard')
        else:
            return resolve_url('doctor_dashboard')
