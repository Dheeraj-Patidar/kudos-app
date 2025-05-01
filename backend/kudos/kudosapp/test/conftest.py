import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from kudosapp.models import Organization

User = get_user_model()


@pytest.fixture
def organization():
    return Organization.objects.create(name="TestOrg")


@pytest.fixture
def user(organization):
    return User.objects.create_user(
        email="sender@example.com",
        password="testpass123",
        organization=organization,
        first_name="Sender",
        last_name="User",
    )


@pytest.fixture
def receiver(organization):
    return User.objects.create_user(
        email="receiver@example.com",
        password="testpass123",
        organization=organization,
        first_name="Receiver",
        last_name="User",
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(client, user):
    response = client.post(
        "/api/login/", {"email": user.email, "password": "testpass123"}
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client
