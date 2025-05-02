import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS, connections
from kudosapp.models import Organization
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture(scope="session")
def create_test_db():
    """
    Set up the test database at the beginning of the test session,
    and tear it down at the end.
    """
    # Ensure the test database is set up and migrations are applied
    call_command("migrate", database=DEFAULT_DB_ALIAS)

    yield

    with connections["default"].cursor() as cursor:
        cursor.execute("DROP DATABASE IF EXISTS test_kudos_db;")
        connections["default"].close()


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
