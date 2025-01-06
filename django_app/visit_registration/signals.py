from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import PatientProfile, DoctorProfile, Specialization

Group.objects.get_or_create(name="patient")
Group.objects.get_or_create(name='doctor')

@receiver(m2m_changed, sender=User.groups.through)
def create_patient_profile_on_group_add(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        patient_group, _ = Group.objects.get_or_create(name="patient")
        doctor_group, _ = Group.objects.get_or_create(name='doctor')
        if patient_group.pk in pk_set:
            PatientProfile.objects.get_or_create(user=instance)
        if doctor_group.pk in pk_set:
            DoctorProfile.objects.create(user=instance, specialization=Specialization.objects.get_or_create(name='lekarz')[0])
