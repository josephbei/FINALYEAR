from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('discipline', 'Discipline'),
        ('headmaster', 'Headmaster'),
        ('parent', 'Parent'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Student(models.Model):
    reg_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')

    @property
    def parent_email(self):
        return self.parent.email

    @property
    def parent_phone(self):
        return self.parent.phone

    def __str__(self):
        return f"{self.reg_number} - {self.name}"

class PermissionRequest(models.Model):
    TYPE_CHOICES = [('normal', 'Normal'), ('emergency', 'Emergency')]
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('escalated', 'Escalated'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='permissions')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    permission_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='normal')
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_permissions')
    processed_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    exit_pass = models.FileField(upload_to='exit_passes/', null=True, blank=True)

    def set_status(self, new_status, user=None, note=''):
        self.status = new_status
        self.processed_by = user
        self.processed_at = timezone.now()
        self.note = note
        self.save()
        from .utils import notify_parent_on_status_change, generate_exit_pass_pdf
        if new_status == 'approved':
            pdf_path = generate_exit_pass_pdf(self)
            if pdf_path:
                self.exit_pass.name = pdf_path
                self.save()
        notify_parent_on_status_change(self)

    def get_download_url(self):
        if self.exit_pass:
            from django.urls import reverse
            return reverse('permission_download', args=[str(self.id)])
        return None

    def __str__(self):
        return f"{self.student} - {self.permission_type} - {self.status}"
