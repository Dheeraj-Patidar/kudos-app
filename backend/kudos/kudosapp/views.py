from rest_framework import generics, permissions
from .models import User, Kudos, Organization
from .serializers import UserSerializer, KudosSerializer, OrganizationSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class SignupView(generics.CreateAPIView):
    """signup users"""
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer


class OrganizationView(generics.CreateAPIView):
    """create organizations """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrganizationListView(generics.ListAPIView):
    """list all organizations"""
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


# List Users in the Same Organization
class UserListView(generics.ListAPIView):
    """list all users which belongs to same organization"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(organization=self.request.user.organization)


# List Kudos received by the logged-in user
class KudosReceivedListView(generics.ListAPIView):
    """displaying all its kudos to the logged in user"""
    serializer_class = KudosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Kudos.objects.filter(receiver=self.request.user)


# Create Kudos (with auto-sender field)

class KudosCreateView(generics.CreateAPIView):
    serializer_class = KudosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)  # Only set sender


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Ensure the currently authenticated user is updated."""
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """Override update to return a success message."""
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Password updated successfully!"})