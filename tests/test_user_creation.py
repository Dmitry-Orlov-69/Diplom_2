import pytest
import requests
import random
import string
import allure

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@yandex.ru'

def random_name():
    return ''.join(random.choices(string.ascii_letters, k=8))

class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_user_creation(self):
        with allure.step("Генерация данных пользователя"):
            email = random_email()
            password = 'testpassword'
            name = random_name()

        with allure.step("Регистрация пользователя"):
            response = requests.post(
                'https://stellarburgers.education-services.ru/api/auth/register',
                json={
                    "email": email,
                    "password": password,
                    "name": name
                }
            )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, unique_user):
        with allure.step("Получение данных существующего пользователя"):
            email = unique_user['user_data']['email']
            password = unique_user['user_data']['password']
            name = unique_user['user_data']['name']

        with allure.step("Попытка создать пользователя с уже существующим email"):
            response = requests.post(
                'https://stellarburgers.education-services.ru/api/auth/register',
                json={
                    "email": email,
                    "password": password,
                    "name": name
                }
            )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] is False
        assert "User already exists" in response_data['message']

    @allure.title("Создание пользователя с незаполненным обязательным полем")
    def test_create_user_with_missing_field(self):
        with allure.step("Генерация данных для пользователя (намеренно не заполняем поле name)"):
            email = random_email()
            password = 'testpassword'

        with allure.step("Попытка регистрации пользователя без заполнения поля name"):
            response = requests.post(
                'https://stellarburgers.education-services.ru/api/auth/register',
                json={
                    "email": email,
                    "password": password,
                }
            )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] is False
        assert "Email, password and name are required fields" in response_data['message']