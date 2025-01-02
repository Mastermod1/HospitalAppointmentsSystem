from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class VisitsEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"visits": ["none", "none"]})
