import allure
import requests
from config import BASE_URL, Endpoints
from src.helpers import generate_user_data


@allure.feature("Создание пользователя")
class TestUserRegister:

    @allure.title("Успешная регистрация нового пользователя")
    def test_register_success(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        assert token is not None

    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user_fail(self):
        user_data = generate_user_data()
        requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Регистрация без email возвращает ошибку")
    def test_register_no_email_fail(self):
        user_data = generate_user_data()
        del user_data["email"]
        response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        assert response.status_code == 403
        assert "required fields" in response.json()["message"]

    @allure.title("Регистрация без password возвращает ошибку")
    def test_register_no_password_fail(self):
        user_data = generate_user_data()
        del user_data["password"]
        response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        assert response.status_code == 403
        assert "required fields" in response.json()["message"]

    @allure.title("Регистрация без name возвращает ошибку")
    def test_register_no_name_fail(self):
        user_data = generate_user_data()
        del user_data["name"]
        response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        assert response.status_code == 403
        assert "required fields" in response.json()["message"]