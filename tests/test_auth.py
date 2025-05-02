import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_signup(api_client):
    url = '/api/signup/'
    data = {
        'username': 'user',
        'password': 'password'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert User.objects.filter(username='user').exists()

@pytest.mark.django_db
def test_login(api_client, test_user):
    url = '/api/token/'
    data = {
        'username': test_user.username,
        'password': "password"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
