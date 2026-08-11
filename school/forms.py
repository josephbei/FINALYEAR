from django import forms
from django.contrib.auth.models import User
from .models import Parent, Student, PermissionRequest

class ParentRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('Username already taken')
        return u

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
        parent = Parent.objects.create(user=user, name=data['name'], email=data['email'], phone=data['phone'])
        # Optionally, create Profile with role parent
        from .models import Profile
        Profile.objects.create(user=user, role='parent')
        return user, parent

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['reg_number', 'name', 'parent']

class PermissionRequestForm(forms.ModelForm):
    class Meta:
        model = PermissionRequest
        fields = ['student', 'permission_type', 'reason']
