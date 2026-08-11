from django.contrib import admin
from .models import Profile, Parent, Student, PermissionRequest

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(PermissionRequest)
