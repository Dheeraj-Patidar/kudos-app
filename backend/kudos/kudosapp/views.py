from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .models import Kudos, Organization, User
from .serializers import (
    KudosRemainingSerializer,
    KudosSerializer,
    OrganizationSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
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
            raise ValidationError(
                {
                    "non_field_errors": [
                        "You have no kudos left to give. please try after 7 days"
                    ]
                }
            )

        self.request.user.kudos_count -= 1
        self.request.user.save(update_fields=["kudos_count"])
        serializer.save(
            sender=self.request.user,
            sender_first_name=self.request.user.first_name,
            sender_last_name=self.request.user.last_name,
            receiver=receiver,
        )
        return Response({"message": "Kudos sent successfully!"})


class KudosRemainingView(generics.RetrieveAPIView):
    serializer_class = KudosRemainingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LatestKudosView(generics.ListAPIView):
    serializer_class = KudosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # Get the logged-in user
        return Kudos.objects.filter(receiver=user).order_by("-timestamp")[
            :5
        ]  # Fetch latest 5 kudos


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token

            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST
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
        super().update(request, *args, **kwargs)

        # Safely get refresh token from request
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            {"message": "Password updated successfully! Please login again"}
        )


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # Generate token & UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            # Send reset email
            send_mail(
                "Password Reset Request",
                f"Click the link below to reset your password: {reset_url}",
                "noreply@kudosapp.com",
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Password reset link sent!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"token": ["Invalid or expired token."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"message": "Password reset successful"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
