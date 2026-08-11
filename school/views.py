from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ParentRegistrationForm, StudentRegistrationForm, PermissionRequestForm
from .models import PermissionRequest, Student, Parent, Profile
from django.http import FileResponse, HttpResponseForbidden
import os

def home(request):
    return render(request, 'school/home.html')

def parent_register(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            user, parent = form.save()
            # auto login parent
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
            return redirect('parent_dashboard')
    else:
        form = ParentRegistrationForm()
    return render(request, 'school/parent_register.html', {'form': form})

@login_required
def parent_dashboard(request):
    # parents see their children and can create emergency permission requests
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'parent':
        return HttpResponseForbidden('Only parents can access this page')
    parent = get_object_or_404(Parent, user=request.user)
    students = parent.students.all()
    return render(request, 'school/parent_dashboard.html', {'parent': parent, 'students': students})

@login_required
def student_register(request):
    # Only staff or parent can create students. Students get no login.
    profile = getattr(request.user, 'profile', None)
    if profile and profile.role in ('teacher', 'discipline', 'headmaster'):
        allowed = True
    elif profile and profile.role == 'parent':
        allowed = True
    else:
        allowed = False
    if not allowed:
        return HttpResponseForbidden('Only staff or parents can register students')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentRegistrationForm()
    return render(request, 'school/student_register.html', {'form': form})

@login_required
def create_permission_request(request):
    profile = getattr(request.user, 'profile', None)
    if request.method == 'POST':
        form = PermissionRequestForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.requested_by = request.user
            pr.save()
            return redirect('home')
    else:
        form = PermissionRequestForm()
        # If parent, restrict student choices to their children
        if profile and profile.role == 'parent':
            parent = get_object_or_404(Parent, user=request.user)
            form.fields['student'].queryset = parent.students.all()
    return render(request, 'school/create_permission.html', {'form': form})

@login_required
def teacher_dashboard(request):
    qs = PermissionRequest.objects.filter(permission_type='normal', status='pending')
    return render(request, 'school/teacher_dashboard.html', {'requests': qs})

@login_required
def discipline_dashboard(request):
    qs = PermissionRequest.objects.filter(permission_type='emergency', status='pending')
    return render(request, 'school/discipline_dashboard.html', {'requests': qs})

@login_required
def process_permission(request, pk):
    perm = get_object_or_404(PermissionRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '')
        user = request.user
        profile = getattr(user, 'profile', None)
        role = profile.role if profile else None
        if perm.permission_type == 'normal' and role != 'teacher':
            return HttpResponseForbidden("Only teachers can process normal permissions.")
        if perm.permission_type == 'emergency' and role not in ('discipline', 'headmaster'):
            return HttpResponseForbidden("Only discipline or headmaster can process emergency permissions.")

        if action == 'approve':
            perm.set_status('approved', user=user, note=note)
        elif action == 'reject':
            perm.set_status('rejected', user=user, note=note)
        elif action == 'escalate':
            perm.set_status('escalated', user=user, note=note)
        return redirect(request.POST.get('next') or '/')
    return render(request, 'school/process_permission.html', {'perm': perm})

@login_required
def download_exit_pass(request, pk):
    perm = get_object_or_404(PermissionRequest, pk=pk)
    if not perm.exit_pass:
        return HttpResponseForbidden("No exit pass available.")
    file_path = perm.exit_pass.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
