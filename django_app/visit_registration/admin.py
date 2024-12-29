from django.contrib import admin
from .models import Appointment, Doctor, Patient, VisitStatus, Specialization

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(VisitStatus)
admin.site.register(Specialization)
