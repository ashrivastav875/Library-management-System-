"""
Accounts app views.
"""
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserAdminSerializer
)
from .permissions import IsAdministrator

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    Public access - creates a new Member user.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Current user profile endpoint.
    GET: Retrieve current user's profile
    PUT/PATCH: Update current user's profile
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    Admin endpoint for managing users.
    Only Administrators can access.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdministrator]
    filter_backends = []  # Disable search/ordering/pagination in Swagger
    pagination_class = None  # Simple list

    def get_queryset(self):
        return User.objects.prefetch_related('groups').order_by('-created_at')
