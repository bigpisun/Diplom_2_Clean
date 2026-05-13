import pytest
import requests
from config import BASE_URL, Endpoints
from src.helpers import generate_user_data


@pytest.fixture
def create_and_delete_user():
    user_data = generate_user_data()
    response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
    assert response.status_code == 200, "Не удалось создать пользователя"
    token = response.json().get("accessToken")
    
    yield user_data, token
    
    # Удаляем пользователя
    if token:
        headers = {"Authorization": token}
        requests.delete(f"{BASE_URL}{Endpoints.LOGOUT}", headers=headers)