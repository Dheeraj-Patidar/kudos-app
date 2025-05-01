import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_list(auth_client):
    url = reverse("user-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
