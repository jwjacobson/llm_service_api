import pytest
from unittest.mock import patch, MagicMock

def test_welcome_view(api_client):
    response = api_client.get('/api/')
    assert response.status_code == 200
    assert response.data['message'] == 'Welcome to the LLM API!'

@pytest.mark.django_db
@patch('llm_api.views.get_provider')
def test_supported_models_view(mock_get_provider, auth_client):
    mock_provider = MagicMock()
    mock_provider.list_models.return_value = ["model-a", "model-b"]
    mock_get_provider.return_value = mock_provider

    response = auth_client.get('/api/supported-models/?provider=openai')
    assert response.status_code == 200
    assert response.data == ["model-a", "model-b"]
