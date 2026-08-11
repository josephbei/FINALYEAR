from rest_framework import serializers
from .models import Parent, Student, PermissionRequest
from django.contrib.auth.models import User

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'name', 'email', 'phone']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ParentRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'], email=validated_data['email'])
        parent = Parent.objects.create(user=user, name=validated_data['name'], email=validated_data['email'], phone=validated_data['phone'])
        from .models import Profile
        Profile.objects.create(user=user, role='parent')
        return parent

class StudentSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='parent', queryset=Parent.objects.all(), write_only=True)
    class Meta:
        model = Student
        fields = ['id', 'reg_number', 'name', 'parent', 'parent_id']

class PermissionRequestSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(source='student', queryset=Student.objects.all(), write_only=True)
    class Meta:
        model = PermissionRequest
        fields = ['id', 'student', 'student_id', 'permission_type', 'reason', 'status', 'created_at']
