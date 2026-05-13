import allure
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

    @allure.title("Вход с неверным паролем возвращает ошибку")
    def test_login_wrong_password_fail(self):
        user_data = generate_user_data()
        requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        
        response = requests.post(
            f"{BASE_URL}{Endpoints.LOGIN}",
            json={"email": user_data["email"], "password": "wrong_password"}
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]

    @allure.title("Вход с несуществующим email возвращает ошибку")
    def test_login_nonexistent_email_fail(self):
        response = requests.post(
            f"{BASE_URL}{Endpoints.LOGIN}",
            json={"email": "nonexistent@example.com", "password": "123456"}
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]