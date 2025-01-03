from django.contrib import admin
from .models import Appointment, DoctorProfile, PatientProfile, VisitStatus, Specialization

# Register your models here.
admin.site.register(Appointment)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(VisitStatus)
admin.site.register(Specialization)
