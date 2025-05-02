def test_welcome_view(api_client):
    response = api_client.get('/api/')
    assert response.status_code == 200
    assert response.data['message'] == 'Welcome to the LLM API!'
