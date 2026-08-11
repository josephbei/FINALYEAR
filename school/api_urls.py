from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('students', api.StudentViewSet, basename='student')
router.register('permissions', api.PermissionRequestViewSet, basename='permission')

urlpatterns = [
    path('parents/register/', api.ParentRegistrationAPIView.as_view(), name='api_parent_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
