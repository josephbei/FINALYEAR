from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ParentRegistrationForm, StudentRegistrationForm, PermissionRequestForm
from .models import PermissionRequest, Student, Parent, Profile
from django.http import FileResponse, HttpResponseForbidden
import os

@login_required
def download_exit_pass(request, pk):
    perm = get_object_or_404(PermissionRequest, pk=pk)
    parent_user = getattr(perm.student.parent, 'user', None)
    # allow if request.user is parent user or is staff (Profile role teacher/discipline/headmaster or is_superuser)
    profile = getattr(request.user, 'profile', None)
    allowed_staff_roles = ('teacher', 'discipline', 'headmaster')
    if request.user == parent_user or (profile and profile.role in allowed_staff_roles) or request.user.is_superuser:
        if not perm.exit_pass:
            return HttpResponseForbidden("No exit pass available.")
        # If using S3 storage, Django's FileField may not have a local path; use .open() and serve
        try:
            f = perm.exit_pass.open('rb')
            response = FileResponse(f, as_attachment=True, filename=os.path.basename(perm.exit_pass.name))
            return response
        except Exception:
            return HttpResponseForbidden("Could not open file.")
    return HttpResponseForbidden("Not authorized")

# keep other views unchanged (home, parent_register, etc.)
from .views import home, parent_register, parent_dashboard, student_register, create_permission_request, teacher_dashboard, discipline_dashboard, process_permission
