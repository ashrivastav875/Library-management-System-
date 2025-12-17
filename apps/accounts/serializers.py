"""
Accounts app serializers.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    email = serializers.EmailField(help_text="e.g. john@example.com")
    username = serializers.CharField(help_text="e.g. johndoe")
    first_name = serializers.CharField(help_text="e.g. John")
    last_name = serializers.CharField(help_text="e.g. Doe")
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Minimum 8 characters"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Must match password"
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""
    groups = serializers.StringRelatedField(many=True, read_only=True)
    is_administrator = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'groups', 'is_administrator', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_administrator']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin user management."""
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )
    is_administrator = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'groups', 'is_administrator', 'is_active', 'is_staff', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_administrator']
