from django.contrib.auth.models import User
from django.db import models


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Specialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return "{} {} - {}".format(self.user.first_name, self.user.last_name, self.specialization.name)


class VisitStatus(models.Model):
    STATUS = [
        ('reserved', 'Reserved'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('moved', 'Moved'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return self.status


class Appointment(models.Model):
    date = models.DateTimeField()
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    status = models.ForeignKey(VisitStatus, on_delete=models.CASCADE, related_name='appointments')
    place = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name} with {self.patient.user.first_name} on {self.date}"
