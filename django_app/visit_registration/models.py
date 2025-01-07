from django.contrib.auth.models import User
from django.db import models


class Specialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return "{} {} - {}".format(self.user.first_name, self.user.last_name, self.specialization.name)


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Appointment(models.Model):
    date = models.DateTimeField()
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed')])
    place = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name} with {self.patient.user.first_name} on {self.date}"


class Visit(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="visit")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="visit")
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='visit')
    interview = models.TextField()
    recommendations = models.TextField()

    def __str__(self):
        return f"Patient_{self.patient.id} With Doctor_{self.doctor.id} On {self.appointment.date}"
