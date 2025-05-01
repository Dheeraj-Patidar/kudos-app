import pytest
from django.urls import reverse
from rest_framework import status
from django.core import mail
import re


@pytest.mark.django_db
def test_password_reset_request(client, user):
    url = reverse("password_reset")
    response = client.post(url, {"email": user.email})
    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) == 1
    assert "Password reset link sent" in response.data["message"]


@pytest.mark.django_db
def test_password_reset_request_invalid_email(client):
    url = reverse("password_reset")
    response = client.post(url, {"email": "invalid@example"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Enter a valid email address." in response.data['email']


@pytest.mark.django_db  
def test_password_reset_request_empty_email(client):
    url = reverse("password_reset")
    response = client.post(url, {"email": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in str(response.data['email'])


@pytest.mark.django_db
def test_password_reset_confirm(client, user):
    # Simulate sending the email and getting the token
    url = reverse("password_reset")
    client.post(url, {"email": user.email})

    assert len(mail.outbox) == 1
    body = mail.outbox[0].body
    match = re.search(r'/reset-password/(?P<uid>[\w\-]+)/(?P<token>[\w\-]+)/', body)
    assert match, f"Could not extract UID and token from email body: {body}"
    uid = match.group("uid")
    token = match.group("token")

    confirm_url = reverse("password_reset_confirm", args=[uid, token])
    response = client.post(confirm_url, {
        
        "new_password": "newpassword123",
    })
    assert response.status_code == status.HTTP_200_OK
    assert "Password reset successful" in response.data['message']


@pytest.mark.django_db
def test_password_reset_confirm_invalid_token(client, user):
    # Simulate sending the email and getting the token
    url = reverse("password_reset")
    client.post(url, {"email": user.email})

    assert len(mail.outbox) == 1
    body = mail.outbox[0].body
    match = re.search(r'/reset-password/(?P<uid>[\w\-]+)/(?P<token>[\w\-]+)/', body)
    assert match, f"Could not extract UID and token from email body: {body}"
    uid = match.group("uid")
    token = "invalid-token"

    confirm_url = reverse("password_reset_confirm", args=[uid, token])
    response = client.post(confirm_url, {
        "new_password": "newpassword123",
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid or expired token." in response.data['token']


@pytest.mark.django_db
def test_password_reset_confirm_empty_password(client, user):
    # Simulate sending the email and getting the token
    url = reverse("password_reset")
    client.post(url, {"email": user.email})

    assert len(mail.outbox) == 1
    body = mail.outbox[0].body
    match = re.search(r'/reset-password/(?P<uid>[\w\-]+)/(?P<token>[\w\-]+)/', body)
    assert match, f"Could not extract UID and token from email body: {body}"
    uid = match.group("uid")
    token = match.group("token")

    confirm_url = reverse("password_reset_confirm", args=[uid, token])
    response = client.post(confirm_url, {
        "new_password": "",
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in str(response.data['new_password'])


@pytest.mark.django_db
def test_password_reset_confirm_invalid_uid(client, user):
    # Simulate sending the email and getting the token
    url = reverse("password_reset")
    client.post(url, {"email": user.email})

    assert len(mail.outbox) == 1
    body = mail.outbox[0].body
    match = re.search(r'/reset-password/(?P<uid>[\w\-]+)/(?P<token>[\w\-]+)/', body)
    assert match, f"Could not extract UID and token from email body: {body}"
    uid = "invalid-uid"
    token = match.group("token")

    confirm_url = reverse("password_reset_confirm", args=[uid, token])
    response = client.post(confirm_url, {
        "new_password": "newpassword123",
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid user." in response.data['error']


@pytest.mark.django_db
def test_change_password(auth_client, user):
    url = reverse("reset-password")
    # client.force_authenticate(user=user)
    response = auth_client.patch(url, {
        "old_password": "testpass123",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    })
    assert response.status_code == status.HTTP_200_OK
    assert "Password updated successfully! Please login again" in response.data['message']


@pytest.mark.django_db
def test_change_password_invalid_old_password(auth_client, user):
    url = reverse("reset-password")
    response = auth_client.patch(url, {
        "old_password": "wrongpassword",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Old password is incorrect." in response.data['old_password']


@pytest.mark.django_db
def test_change_password_mismatch(auth_client, user):
    url = reverse("reset-password")
    response = auth_client.patch(url, {
        "old_password": "testpass123",
        "new_password": "newpassword123",
        "confirm_password": "differentpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Passwords do not match." in response.data['confirm_password']

    
@pytest.mark.django_db
def test_change_password_empty_fields(auth_client, user):
    url = reverse("reset-password")
    response = auth_client.patch(url, {
        "old_password": "",
        "new_password": "",
        "confirm_password": ""
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in str(response.data['old_password'])
    assert "This field may not be blank." in str(response.data['new_password'])
    assert "This field may not be blank." in str(response.data['confirm_password'])


@pytest.mark.django_db
def test_change_password_invalid_new_password(auth_client, user):
    url = reverse("reset-password")
    response = auth_client.patch(url, {
        "old_password": "testpass123",
        "new_password": "short",
        "confirm_password": "short"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Password must be at least 8 characters long." in response.data['new_password']

