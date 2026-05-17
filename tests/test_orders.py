import allure
import pytest
import requests
from config import BASE_URL, Endpoints
from src.data import VALID_INGREDIENTS

@allure.feature("Получение заказов пользователя")
class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth_success(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        headers = {"Authorization": token}
        
        # Сначала создадим заказ для этого пользователя, чтобы список не был пустым
        requests.post(
            f"{BASE_URL}{Endpoints.CREATE_ORDER}",
            json={"ingredients": VALID_INGREDIENTS},
            headers=headers
        )

        # Выполняем GET запрос на получение заказов
        response = requests.get(f"{BASE_URL}{Endpoints.CREATE_ORDER}", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert len(response.json()["orders"]) > 0

    @allure.title("Получение заказов неавторизованного пользователя возвращает ошибку")
    def test_get_orders_without_auth_fail(self):
        response = requests.get(f"{BASE_URL}{Endpoints.CREATE_ORDER}")
        
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == "You should be authorised"