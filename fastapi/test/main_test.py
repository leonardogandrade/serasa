from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@patch('requests.get')
def test_users_endpoint_success(mock_get):
    
    mock_response = type('MockResponse', (), {
        'json': lambda self: {"data": "mocked response"},
        'status_code': 200
    })()
    
    mock_get.return_value = mock_response

    response = client.get("/users?nome=John")
    
    assert response.status_code == 200
    assert response.json() == {"message": {"data": "mocked response"}}
    mock_get.assert_called_once_with("http://flask-api:5000/get_data?nome=John")
