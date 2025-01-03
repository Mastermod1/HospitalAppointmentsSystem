from django.shortcuts import render, resolve_url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.models import Token


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


@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    response = render(request, 'patient_dashboard.html')
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    response.set_cookie('auth_token', token, max_age=3600)
    return response


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    response = render(request, 'doctor_dashboard.html')
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    response.set_cookie('auth_token', token, max_age=3600)
    return response


class CustomLoginView(LoginView):
    def get_success_url(self):
        if is_doctor(self.request.user):
            return resolve_url('doctor_dashboard')
        if is_patient(self.request.user):
            return resolve_url('patient_dashboard')
        else:
            return resolve_url('doctor_dashboard')
