from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Kudos, Organization, User
from .serializers import (
    KudosSerializer,
    OrganizationSerializer,
    ResetPasswordSerializer,
    SignupSerializer,
    UserSerializer,
)


class SignupView(generics.CreateAPIView):
    """signup users"""

    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer


class OrganizationView(generics.CreateAPIView):
    """create organizations"""

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


class KudosCreateView(generics.CreateAPIView):
    """create kudos for the user"""

    queryset = Kudos.objects.all()
    serializer_class = KudosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_email = self.request.data.get("receiver")

        try:
            receiver = User.objects.get(email=receiver_email)
        except User.DoesNotExist:
            raise ValidationError({"receiver": "Receiver not found."})

        seven_days_ago = timezone.now() - timedelta(days=7)
        kudos_count = Kudos.objects.filter(
            sender=self.request.user, timestamp__gte=seven_days_ago
        ).count()

        if kudos_count >= 3:
            raise ValidationError("You can only give 3 kudos in 7 days.")

        serializer.save(sender=self.request.user, receiver=receiver)
        return Response({"message": "Kudos sent successfully!"})


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token

            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"error": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordView(generics.UpdateAPIView):
    """reset password for the user"""

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
