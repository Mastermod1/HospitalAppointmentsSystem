from django.contrib import admin
from .models import Appointment, DoctorProfile, PatientProfile, Specialization, Visit


admin.site.register(Appointment)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(Specialization)
admin.site.register(Visit)
