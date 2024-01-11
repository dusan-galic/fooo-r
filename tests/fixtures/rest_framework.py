import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_user_client1(api_client, user1):
    """Rest API client with authenticated user."""
    api_client.force_authenticate(user1)
    return api_client


@pytest.fixture
def api_user_client2(api_client, user2):
    """Rest API client with authenticated user."""
    api_client.force_authenticate(user2)
    return api_client
