import allure
import requests
from config import BASE_URL, Endpoints
from src.helpers import generate_user_data
from src.data import VALID_INGREDIENTS, INVALID_HASH


@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self):
        # Регистрируем пользователя
        user_data = generate_user_data()
        register_response = requests.post(f"{BASE_URL}{Endpoints.REGISTER}", json=user_data)
        assert register_response.status_code == 200
        token = register_response.json()["accessToken"]
        
        headers = {"Authorization": token}
        response = requests.post(
            f"{BASE_URL}{Endpoints.CREATE_ORDER}",
            json={"ingredients": VALID_INGREDIENTS},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self):
        response = requests.post(
            f"{BASE_URL}{Endpoints.CREATE_ORDER}",
            json={"ingredients": VALID_INGREDIENTS}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов возвращает ошибку")
    def test_create_order_no_ingredients_fail(self):
        response = requests.post(
            f"{BASE_URL}{Endpoints.CREATE_ORDER}",
            json={"ingredients": []}
        )
        assert response.status_code == 400
        assert "must be provided" in response.json()["message"]

    @allure.title("Создание заказа с неверным хешем ингредиента возвращает ошибку 500")
    def test_create_order_invalid_hash_fail(self):
        response = requests.post(
            f"{BASE_URL}{Endpoints.CREATE_ORDER}",
            json={"ingredients": [INVALID_HASH]}
        )
        assert response.status_code == 500