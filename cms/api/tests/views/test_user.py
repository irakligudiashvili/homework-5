import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from api.models import User


@pytest.mark.django_db
def test_user_registration_success():
    client = APIClient()
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "securepassword",
        "role": "student"
    }

    response = client.post("/api/v1/auth/register/", data, format="json")

    assert response.status_code == HTTP_201_CREATED
    assert response.data["message"] == "User created successfully"
    assert User.objects.filter(email="john@example.com").exists()


@pytest.mark.django_db
def test_user_registration_missing_fields():
    client = APIClient()
    data = {
        "first_name": "Jane",
        "email": "jane@example.com",
        "password": "securepassword",
        "role": "student"
    }

    response = client.post("/api/v1/auth/register/", data, format="json")

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "last_name" in response.data
    assert not User.objects.filter(email="jane@example.com").exists()


@pytest.mark.django_db
def test_user_registration_invalid_role():
    client = APIClient()
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "password": "securepassword",
        "role": "invalid_role"
    }

    response = client.post("/api/v1/auth/register/", data, format="json")

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert "role" in response.data
    assert not User.objects.filter(email="alice@example.com").exists()
