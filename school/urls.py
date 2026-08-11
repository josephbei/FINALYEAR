from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parent/register/', views.parent_register, name='parent_register'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('student/register/', views.student_register, name='student_register'),
    path('permission/create/', views.create_permission_request, name='create_permission'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('discipline/', views.discipline_dashboard, name='discipline_dashboard'),
    path('permission/<uuid:pk>/process/', views.process_permission, name='process_permission'),
    path('permission/<uuid:pk>/download/', views.download_exit_pass, name='permission_download'),
]
