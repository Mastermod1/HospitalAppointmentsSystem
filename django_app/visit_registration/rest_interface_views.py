from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Specialization, Doctor
from .serializers import SpecializationSerializer, DoctorSerializer


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
            doctors = Doctor.objects.filter(specialization__id=specialization_id)

            if not doctors.exists():
                return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)

            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Specialization.DoesNotExist:
            return Response({"error": "error"}, status=status.HTTP_404_NOT_FOUND)
