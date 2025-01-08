import json
from datetime import datetime, time, timedelta, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Specialization, DoctorProfile, Appointment, PatientProfile, Visit
from .serializers import SpecializationSerializer, DoctorProfileSerializer, AppointmentSerializer, VisitSerializer
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method

DATE_FORMAT_STRING = "%d.%m.%Y"
TIME_FORMAT_STRING = "%H:%M"
DATETIME_FORMAT_STRING = f"{DATE_FORMAT_STRING} {TIME_FORMAT_STRING}"


class SpecializationsEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get specializations.",
        responses={
            200: VisitSerializer(many=True, help_text="Get specializations."),
        }
    )
    def get(self, request):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get doctors.",
        responses={
            200: VisitSerializer(many=True, help_text="Get doctors."),
            404: VisitSerializer(many=True, help_text="Not found doctors."),
        }
    )
    def get(self, request, specialization_id):
        try:
            doctors = DoctorProfile.objects.filter(specialization__id=specialization_id)

            if not doctors.exists():
                return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)

            serializer = DoctorProfileSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)


class DoctorAvailabilityEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get doctor availability.",
        responses={
            200: VisitSerializer(many=True, help_text="Get doctor availability."),
            404: VisitSerializer(many=True, help_text="Not found appointments."),
        }
    )
    def get(self, request, doctor_id, date):
        try:
            datetime_date = datetime.strptime(date, "%Y-%m-%d").date()
            appointments = Appointment.objects.filter(doctor__id=doctor_id, date__date=datetime_date)

            reserved_times = [x.date for x in appointments]
            start = datetime.combine(datetime_date, time(hour=8, minute=0)).replace(tzinfo=timezone.utc)
            free_times = []
            while (start != datetime.combine(datetime_date, time(hour=16, minute=0).replace(tzinfo=timezone.utc))):
                if start not in reserved_times:
                    free_times.append(start.strftime(DATETIME_FORMAT_STRING))
                start = start + timedelta(minutes=30)
            res = {"times": free_times}

            return Response(json.dumps(res, indent=4), status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)


class AppointmentEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create an appointment.",
        responses={
            201: VisitSerializer(many=True, help_text="Create an appointment."),
            400: VisitSerializer(many=True, help_text="Missing argument or incorrect appointment date."),
            404: VisitSerializer(many=True, help_text="Something not available in database."),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        doctor_id = request.data.get('doctor_id')
        appointment_date = request.data.get('time')

        if not doctor_id or not appointment_date:
            return Response({"error": "Doctor ID and date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            print('No DoctorProfile', flush=True)
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            patient = PatientProfile.objects.get(user=user)
        except PatientProfile.DoesNotExist:
            print('No Patient', flush=True)
            return Response({"error": "Patient not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        try:
            appointment_date = datetime.strptime(appointment_date, DATETIME_FORMAT_STRING)
        except ValueError:
            print('No Date', flush=True)
            return Response({"error": "Invalid date format. Use ctime eg: Sun Jan  5 08:00:00 2025"}, status=status.HTTP_400_BAD_REQUEST)

        if appointment_date <= datetime.now():
            print('Bad date', flush=True)
            return Response({"error": "Appointment date must be in the future."}, status=status.HTTP_400_BAD_REQUEST)

        appointment = Appointment.objects.create(patient=patient, doctor=doctor, date=appointment_date, status='scheduled')

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorVisitsEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve ordered appointments ordered by time for doctor.",
        responses={
            200: VisitSerializer(many=True, help_text="Retrieve ordered appointments ordered by time for doctor."),
            404: VisitSerializer(many=True, help_text="Doctor does not exist."),
        }
    )
    def get(self, request, date):
        try:
            datetime_date = datetime.strptime(date, DATE_FORMAT_STRING).date()
            doctorProfile = DoctorProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctorProfile, date__date=datetime_date, status="scheduled")
            res = {"appointments": [{"date": x.date.strftime(DATE_FORMAT_STRING), "time": x.date.strftime(TIME_FORMAT_STRING), "patient_name": x.patient.user.get_full_name(), "patient_id": x.patient.id, "appointment_id": x.id} for x in appointments]}
            res["appointments"] = sorted(res["appointments"], key=lambda x: x["time"])
            return Response(json.dumps(res, indent=4), status=status.HTTP_200_OK)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)


class CreateVisit(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a visit from an appointment.",
        responses={
            201: VisitSerializer(many=True, help_text="Created visit."),
            400: VisitSerializer(many=True, help_text="Missing field."),
            404: VisitSerializer(many=True, help_text="Not present in database."),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        patient_id = request.data.get('patient_id', None)
        appointment_id = request.data.get('appointment_id', None)
        interview = request.data.get('interview', None)
        recommendations = request.data.get('recommendations', None)

        if patient_id is None or appointment_id is None or interview is None or recommendations is None:
            return Response({"error": "Missing one field."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = DoctorProfile.objects.get(user=user)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            patient = PatientProfile.objects.get(id=patient_id)
        except PatientProfile.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except PatientProfile.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        visit = Visit.objects.create(patient=patient, doctor=doctor, appointment=appointment, interview=interview, recommendations=recommendations)
        appointment.status = "completed"
        appointment.save()

        serializer = VisitSerializer(visit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
