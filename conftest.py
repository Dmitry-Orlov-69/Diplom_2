import pytest
import requests
import random
import string

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@yandex.ru'

def random_name():
    return ''.join(random.choices(string.ascii_letters, k=8))

@pytest.fixture
def unique_user(request):
    email = random_email()
    password = 'testpassword'
    name = random_name()

    # Регистрация пользователя
    response = requests.post(
        'https://stellarburgers.education-services.ru/api/auth/register',
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

        # Определяем функцию для удаления пользователя после теста
        def delete_user():
            requests.delete(
                'https://stellarburgers.education-services.ru/api/auth/user',
                json={
                    "email": user_data['user_data']['email']
                }
            )

        # Добавляем финализатор для удаления пользователя
        request.addfinalizer(delete_user)

        return user_data
    else:
        raise Exception(f"Failed to create user: {response.text}")