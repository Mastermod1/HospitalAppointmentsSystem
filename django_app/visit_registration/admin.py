from django.contrib import admin
from .models import Appointment, DoctorProfile, PatientProfile, VisitStatus, Specialization


VisitStatus.objects.get_or_create(status="reserved")
Specialization.objects.get_or_create(name="lekarz")


admin.site.register(Appointment)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(VisitStatus)
admin.site.register(Specialization)
