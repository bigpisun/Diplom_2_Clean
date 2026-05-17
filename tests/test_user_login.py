import allure
import pytest
import requests
from config import BASE_URL, Endpoints
from src.helpers import generate_user_data

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный вход существующего пользователя")
    def test_login_success(self):
        user_data = generate_user_data()
        requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        
        response = requests.post(
            f"{BASE_URL}{Endpoints.LOGIN}",
            json={"email": user_data["email"], "password": user_data["password"]}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

        # Очистка внутри теста, чтобы не плодить юзеров
        token = response.json().get("accessToken")
        requests.delete(f"{BASE_URL}{Endpoints.USER}", headers={"Authorization": token})

    @allure.title("Негативные проверки логина: неверные данные")
    @pytest.mark.parametrize(
        "email_modifier, password_modifier, expected_status, expected_message",
        [
            ("correct", "wrong_password", 401, "email or password are incorrect"),
            ("nonexistent@example.com", "123456", 401, "email or password are incorrect")
        ]
    )
    def test_login_fail(self, email_modifier, password_modifier, expected_status, expected_message):
        user_data = generate_user_data()
        register_response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        token = register_response.json().get("accessToken")

        # Определяем, какие данные отправлять на вход
        email = user_data["email"] if email_modifier == "correct" else email_modifier
        password = password_modifier if password_modifier != "correct" else user_data["password"]

        response = requests.post(
            f"{BASE_URL}{Endpoints.LOGIN}",
            json={"email": email, "password": password}
        )
        
        # Сначала удалим созданного пользователя, чтобы не засорять базу
        if token:
            requests.delete(f"{BASE_URL}{Endpoints.USER}", headers={"Authorization": token})

        # Проверяем результаты
        assert response.status_code == expected_status
        assert expected_message in response.json()["message"]