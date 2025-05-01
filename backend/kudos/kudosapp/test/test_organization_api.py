import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_organization(auth_client):
    url = reverse("organization")
    response = auth_client.post(url, {"name": "NewOrg"})
    assert response.status_code == status.HTTP_201_CREATED
    assert "name" in response.data


@pytest.mark.django_db
def test_create_org_with_empty_name(auth_client):
    url = reverse("organization")
    response = auth_client.post(url, {"name": ""})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in str(response.data["name"])


@pytest.mark.django_db
def test_list_organizations(client):
    url = reverse("organization-list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
