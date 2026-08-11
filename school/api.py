from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from .models import Parent, Student, PermissionRequest
from .serializers import ParentRegistrationSerializer, StudentSerializer, PermissionRequestSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

class ParentRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ParentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            parent = serializer.save()
            return Response({'id': parent.id, 'name': parent.name}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

class PermissionRequestViewSet(viewsets.ModelViewSet):
    queryset = PermissionRequest.objects.all().order_by('-created_at')
    serializer_class = PermissionRequestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # set requested_by if user is authenticated
        req = serializer.save()
        return req

