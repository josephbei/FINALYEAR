from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register('students', api.StudentViewSet, basename='student')
router.register('permissions', api.PermissionRequestViewSet, basename='permission')

urlpatterns = [
    path('parents/register/', api.ParentRegistrationAPIView.as_view(), name='api_parent_register'),
    path('', include(router.urls)),
]
