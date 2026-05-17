BASE_URL = "https://stellarburgers.education-services.ru"

class Endpoints:
    REGISTER = "/api/auth/register"
    LOGIN = "/api/auth/login"
    LOGOUT = "/api/auth/logout"
    USER = "/api/auth/user"          # Добавили для PATCH и DELETE запросов к пользователю
    CREATE_ORDER = "/api/orders"     # Он же используется для GET /api/orders (заказы конкретного юзера)
    ALL_ORDERS = "/api/orders/all"   # Добавили для получения всех заказов из системы
    GET_INGREDIENTS = "/api/ingredients"