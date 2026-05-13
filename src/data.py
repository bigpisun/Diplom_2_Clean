import requests
from config import BASE_URL, Endpoints


def get_valid_ingredients():
    response = requests.get(f"{BASE_URL}{Endpoints.GET_INGREDIENTS}")
    data = response.json()
    return [ingredient["_id"] for ingredient in data["data"][:2]]


VALID_INGREDIENTS = get_valid_ingredients()
INVALID_HASH = "invalid_hash_123"