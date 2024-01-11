from django.urls import reverse
from rest_framework import status


def test_login_user(api_client, user1):
    user1.set_password("test12test")
    user1.save()

    response = api_client.post(
        reverse("user_login"),
        data={"email": "testara.testic@test.com", "password": "test12test"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["refresh"]
    assert response_data["access"]


def test_login_user_bad_credentials(api_client, user1):
    user1.set_password("test12test")
    user1.save()

    response = api_client.post(
        reverse("user_login"),
        data={"email": "testara.testic@test.com", "password": "test"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "No active account found with the given credentials"
    }
