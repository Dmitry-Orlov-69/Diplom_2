import pytest
import requests
from helpers import random_email, random_name
from urls import DELETE_USER_ENDPOINT, REGISTER_ENDPOINT

@pytest.fixture
def unique_user():
    email = random_email()
    password = 'testpassword'
    name = random_name()

    # Регистрация пользователя
    response = requests.post(
        REGISTER_ENDPOINT,
        json={
            "email": email,
            "password": password,
            "name": name
        }
    )

    if response.status_code == 200:
        user_data = {
            "user_data": {
                "email": email,
                "password": password,
                "name": name
            },
            "response": response.json()
        }

        # Использование yield для автоматического удаления пользователя после теста
        yield user_data

        # Удаление пользователя после завершения теста
        requests.delete(
            DELETE_USER_ENDPOINT,
            json={
                "email": user_data['user_data']['email']
            }
        )
    else:
        pytest.fail(f"Failed to create user: {response.text}")