import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_signup(client):
    url = reverse("signup")
    payload = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "strongpass123",
        "repassword": "strongpass123",
        "organization": "TestOrg",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert "email" in response.data


@pytest.mark.django_db
def test_signup_with_invalid_email(client):
    url = reverse("signup")
    payload = {
        "email": "invalid-email",
        "first_name": "Test",
        "last_name": "User",
        "password": "strongpass123",
        "repassword": "strongpass123",
        "organization": "TestOrg",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Enter a valid email address." in response.data["email"]


@pytest.mark.django_db
def test_signup_empty_fields(client):
    url = reverse("signup")
    payload = {
        "email": "",
        "first_name": "",
        "last_name": "",
        "password": "",
        "repassword": "",
        "organization": "",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in response.data["email"]
    assert "This field may not be blank." in response.data["first_name"]
    assert "This field may not be blank." in response.data["last_name"]
    assert "This field may not be blank." in response.data["password"]
    assert "This field may not be blank." in response.data["repassword"]
    assert "This field may not be blank." in response.data["organization"]


@pytest.mark.django_db
def test_signup_with_existing_email(client, user):
    url = reverse("signup")
    payload = {
        "email": user.email,
        "first_name": "Test",
        "last_name": "User",
        "password": "strongpass123",
        "repassword": "strongpass123",
        "organization": "TestOrg",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "user with this email already exists." in response.data["email"]


@pytest.mark.django_db
def test_signup_without_email(client):
    url = reverse("signup")
    payload = {
        "email": "",
        "first_name": "Test",
        "last_name": "User",
        "password": "strongpass123",
        "repassword": "strongpass123",
        "organization": "TestOrg",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in response.data["email"]


@pytest.mark.django_db
def test_signup_password_match(client):
    url = reverse("signup")
    payload = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "strongpass12345",
        "repassword": "strongpass123",
        "organization": "TestOrg",
    }
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "password and repassword do not match" in response.data["repassword"]
    )


@pytest.mark.django_db
def test_login(client, user):
    url = reverse("token_obtain_pair")
    payload = {"email": user.email, "password": "testpass123"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_with_invalid_credentials(client, user):
    url = reverse("token_obtain_pair")
    payload = {"email": user.email, "password": "wrongpassword"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        "No active account found with the given credentials"
        in response.data["detail"]
    )


@pytest.mark.django_db
def test_login_with_nonexistent_user(client):
    url = reverse("token_obtain_pair")
    payload = {"email": "wrongemail", "password": "wrongpassword"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        "No active account found with the given credentials"
        in response.data["detail"]
    )


@pytest.mark.django_db
def test_login_with_inactive_user(client, user):
    url = reverse("token_obtain_pair")
    user.is_active = False
    user.save()
    payload = {"email": user.email, "password": "testpass123"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        "No active account found with the given credentials"
        in response.data["detail"]
    )


@pytest.mark.django_db
def test_login_with_invalid_email_format(client):
    url = reverse("token_obtain_pair")
    payload = {"email": "invalid-email", "password": "testpass123"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        "No active account found with the given credentials"
        in response.data["detail"]
    )


@pytest.mark.django_db
def test_login_with_empty_fields(client):
    url = reverse("token_obtain_pair")
    payload = {"email": "", "password": ""}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in response.data["email"]
    assert "This field may not be blank." in response.data["password"]


@pytest.mark.django_db
def test_token_refresh(client, user):
    login_url = reverse("token_obtain_pair")
    refresh_url = reverse("token_refresh")
    login_resp = client.post(
        login_url, {"email": user.email, "password": "testpass123"}
    )
    refresh_token = login_resp.data["refresh"]
    refresh_resp = client.post(refresh_url, {"refresh": refresh_token})
    assert refresh_resp.status_code == status.HTTP_200_OK
    assert "access" in refresh_resp.data


@pytest.mark.django_db
def test_token_refresh_with_invalid_token(client):
    url = reverse("token_refresh")
    payload = {"refresh": "invalidtoken"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Token is invalid or expired" in response.data["detail"]


@pytest.mark.django_db
def test_token_refresh_with_empty_fields(client):
    url = reverse("token_refresh")
    payload = {"refresh": ""}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in response.data["refresh"]


@pytest.mark.django_db
def test_token_refresh_with_nonexistent_user(client):
    url = reverse("token_refresh")
    payload = {"refresh": "nonexistenttoken"}
    response = client.post(url, data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Token is invalid or expired" in response.data["detail"]
