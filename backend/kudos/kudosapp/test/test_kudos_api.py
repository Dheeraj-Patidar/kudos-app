from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from kudosapp.models import Kudos


@pytest.mark.django_db
def test_give_kudos_success(auth_client, receiver, user):
    url = reverse("kudos-create")
    initial_kudos_count = user.kudos_count
    response = auth_client.post(
        url, {"receiver": receiver.email, "message": "You're amazing!"}
    )
    assert (
        response.status_code == status.HTTP_201_CREATED or status.HTTP_200_OK
    )
    user.refresh_from_db()
    assert user.kudos_count == initial_kudos_count - 1


@pytest.mark.django_db
def test_give_kudos_with_empty_message_field(auth_client, receiver):
    url = reverse("kudos-create")
    response = auth_client.post(url, {"receiver": receiver, "message": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in str(response.data["message"])


@pytest.mark.django_db
def test_give_kudos_invalid_receiver(auth_client):
    url = reverse("kudos-create")
    response = auth_client.post(
        url, {"receiver": "invalid_email", "message": "You're amazing!"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "receiver not found" in str(response.data).lower()


@pytest.mark.django_db
def test_give_kudos_to_sender(auth_client, user):
    url = reverse("kudos-create")
    response = auth_client.post(
        url, {"receiver": user.email, "message": "You're amazing!"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "receiver cannot be the sender." in str(response.data).lower()


@pytest.mark.django_db
def test_kudos_limit(auth_client, receiver, user):
    now = timezone.now()
    Kudos.objects.bulk_create(
        [
            Kudos(
                sender=user,
                receiver=receiver,
                message="Test",
                timestamp=now - timedelta(days=7),
            )
            for _ in range(3)
        ]
    )
    url = reverse("kudos-create")
    response = auth_client.post(
        url, {"receiver": receiver.email, "message": "One more"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "no kudos left" in str(response.data).lower()


@pytest.mark.django_db
def test_kudos_received(auth_client, receiver, user):
    Kudos.objects.create(sender=user, receiver=receiver, message="Test Kudos")
    url = reverse("kudos-received")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_kudos_remaining(auth_client):
    url = reverse("kudosremaining")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "kudos_remaining" in response.data
