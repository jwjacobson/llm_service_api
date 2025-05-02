import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    """A basic client."""
    return APIClient()

@pytest.fixture
def test_user():
    """A basic user."""
    return User.objects.create_user(username='user', password='password')

@pytest.fixture
def auth_client(test_user):
    """A client with an authenticated user."""
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client
