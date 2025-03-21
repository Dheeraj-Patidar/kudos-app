from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    KudosCreateView,
    KudosReceivedListView,
    LogoutView,
    OrganizationListView,
    OrganizationView,
    ResetPasswordView,
    SignupView,
    UserListView,
)

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("kudos/", KudosReceivedListView.as_view(), name="kudos-received"),
    path("kudos/give/", KudosCreateView.as_view(), name="kudos-create"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("organization/", OrganizationView.as_view(), name="organization"),
    path(
        "organization/list/",
        OrganizationListView.as_view(),
        name="organization-list",
    ),
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Login
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh Token
    path("logout/", LogoutView.as_view(), name="logout"),  # Logout
    path("reset-password/", ResetPasswordView.as_view(), name="resetpassword"),
]
