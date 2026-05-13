import allure
import requests
from config import BASE_URL


class ApiClient:
    @staticmethod
    @allure.step("Отправка POST запроса на {endpoint}")
    def post(endpoint, data=None, headers=None):
        url = f"{BASE_URL}{endpoint}"
        return requests.post(url, json=data, headers=headers)

    @staticmethod
    @allure.step("Отправка DELETE запроса на {endpoint}")
    def delete(endpoint, headers=None):
        url = f"{BASE_URL}{endpoint}"
        return requests.delete(url, headers=headers)