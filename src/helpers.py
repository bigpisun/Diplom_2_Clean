import random
import string


def generate_random_email():
    return f"test_{random.randint(1000, 9999)}@example.com"


def generate_random_password():
    return f"pass_{random.randint(1000, 9999)}"


def generate_random_name():
    return f"User_{random.randint(1000, 9999)}"


def generate_user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": generate_random_name()
    }