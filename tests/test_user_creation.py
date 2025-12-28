import pytest
import requests
import allure
from helpers import random_email, random_name
from urls import REGISTER_ENDPOINT

class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_user_creation(self):
        with allure.step("Генерация данных пользователя"):
            email = random_email()
            password = 'testpassword'
            name = random_name()

        with allure.step("Регистрация пользователя"):
            response = requests.post(
                REGISTER_ENDPOINT,
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
                REGISTER_ENDPOINT,
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

    @pytest.mark.parametrize("field_to_omit", ["email", "password", "name"])
    @allure.title("Создание пользователя с незаполненным обязательным полем")
    def test_create_user_with_missing_field(field_to_omit):
        with allure.step(f"Генерация данных для пользователя (намеренно не заполняем поле {field_to_omit})"):
            user_data = {
                "email": random_email(),
                "password": "testpassword",
                "name": random_name()
            }
            del user_data[field_to_omit]  # Удаляем поле, которое нужно пропустить

        with allure.step("Попытка регистрации пользователя без заполнения поля"):
            response = requests.post(
                REGISTER_ENDPOINT,
                json=user_data
            )

        assert response.status_code == 403
        response_data = response.json()
        assert response_data['success'] is False
        assert "Email, password and name are required fields" in response_data['message']