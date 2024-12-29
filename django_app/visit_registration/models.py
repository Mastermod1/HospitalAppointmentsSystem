from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Specialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.specialization.name)


class VisitStatus(models.Model):
    STATUS = [
        ('reserved', 'Reserved'),
        ('in_progress', 'In Progress'),
        ('moved', 'Moved'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS)


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    status = models.ForeignKey(VisitStatus, on_delete=models.CASCADE, related_name='appointments')
    place = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name} with {self.patient.first_name} on {self.date} at {self.time}"
