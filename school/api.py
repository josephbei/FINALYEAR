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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Parents see only their students; staff see all
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if profile and profile.role == 'parent':
            parent = Parent.objects.filter(user=user).first()
            return Student.objects.filter(parent=parent)
        return super().get_queryset()

class PermissionRequestViewSet(viewsets.ModelViewSet):
    queryset = PermissionRequest.objects.all().order_by('-created_at')
    serializer_class = PermissionRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if profile and profile.role == 'parent':
            parent = Parent.objects.filter(user=user).first()
            return PermissionRequest.objects.filter(student__parent=parent).order_by('-created_at')
        return super().get_queryset()

    def perform_create(self, serializer):
        # set requested_by to authenticated user
        serializer.save()
