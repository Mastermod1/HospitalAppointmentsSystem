import json
from datetime import datetime, time, timedelta, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Specialization, DoctorProfile, Appointment, PatientProfile, VisitStatus
from .serializers import SpecializationSerializer, DoctorProfileSerializer, AppointmentSerializer
from rest_framework.authtoken.models import Token


class VisitsEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"visits": ["none", "none"]})


class SpecializationsEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, specialization_id):
        try:
            doctors = DoctorProfile.objects.filter(specialization__id=specialization_id)

            if not doctors.exists():
                return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)

            serializer = DoctorProfileSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Specialization.DoesNotExist:
            return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)


class DoctorAvailabilityEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doctor_id, date):
        try:
            datetime_date = datetime.strptime(date, "%Y-%m-%d").date()
            appointments = Appointment.objects.filter(doctor__id=doctor_id, date__date=datetime_date)

            reserved_times = [x.date for x in appointments]
            start = datetime.combine(datetime_date, time(hour=8, minute=0)).replace(tzinfo=timezone.utc)
            free_times = []
            while (start != datetime.combine(datetime_date, time(hour=16, minute=0).replace(tzinfo=timezone.utc))):
                if start not in reserved_times:
                    free_times.append(start.ctime())
                start = start + timedelta(minutes=30)
            res = {"times": free_times}

            return Response(json.dumps(res, indent=4), status=status.HTTP_200_OK)
        except Specialization.DoesNotExist:
            return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)


class AppointmentEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        print(request.data, flush=True)
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
            appointment_date = datetime.strptime(appointment_date, "%a %b %d %H:%M:%S %Y")
        except ValueError:
            print('No Date', flush=True)
            return Response({"error": "Invalid date format. Use ctime eg: Sun Jan  5 08:00:00 2025"}, status=status.HTTP_400_BAD_REQUEST)

        if appointment_date <= datetime.now():
            print('Bad date', flush=True)
            return Response({"error": "Appointment date must be in the future."}, status=status.HTTP_400_BAD_REQUEST)

        status_object = VisitStatus.objects.get(status='reserved')
        appointment = Appointment.objects.create(patient=patient, doctor=doctor, date=appointment_date, place="Poland", status=status_object)

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]  # No authentication or authorization required

    def get(self, request, *args, **kwargs):
        print("halo", flush=True)
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
