from django.db import models

class Appointment(models.Model):
    APPOINTMENT_TYPES = [
        ('general', 'General Consultation'),
        ('followup', 'Follow-Up'),
        ('urgent', 'Urgent Care'),
    ]

    date = models.DateField()
    time = models.TimeField()
    type_of_appointment = models.CharField(max_length=20, choices=APPOINTMENT_TYPES)
    place = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type_of_appointment} on {self.date} at {self.time}"
