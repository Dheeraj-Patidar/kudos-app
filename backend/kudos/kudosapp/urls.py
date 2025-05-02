from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    KudosCreateView,
    KudosReceivedListView,
    KudosRemainingView,
    LatestKudosView,
    LogoutView,
    OrganizationListView,
    OrganizationView,
    PasswordResetConfirmView,
    PasswordResetView,
    ResetPasswordView,
    SignupView,
    UserListView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path(
        "login/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh Token
    path("logout/", LogoutView.as_view(), name="logout"),  # Logout
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("users/", UserListView.as_view(), name="user-list"),
    path("kudos/", KudosReceivedListView.as_view(), name="kudos-received"),
    path("kudos/give/", KudosCreateView.as_view(), name="kudos-create"),
    path("latestkudos/", LatestKudosView.as_view(), name="latestkudos"),
    path("kudosremaining/", KudosRemainingView.as_view(), name="kudosremaining"),
    path("organization/", OrganizationView.as_view(), name="organization"),
    path(
        "organization/list/", OrganizationListView.as_view(), name="organization-list"
    ),
]
