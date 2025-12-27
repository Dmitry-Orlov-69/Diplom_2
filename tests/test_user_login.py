import allure
import requests
from urls import LOGIN_ENDPOINT

class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, unique_user):
        with allure.step("Получение данных существующего пользователя"):
            email = unique_user['user_data']['email']
            password = unique_user['user_data']['password']

        with allure.step("Попытка авторизоваться с существующим пользователем"):
            response = requests.post(
                LOGIN_ENDPOINT,
                json={
                    "email": email,
                    "password": password
                }
            )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert 'accessToken' in response_data

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_incorrect_credentials(self):
        with allure.step("Используем неверные данные для авторизации"):
            email = "nonexistentuser@example.com"
            password = "wrongpassword"

        with allure.step("Попытка авторизоваться с неверными данными"):
            response = requests.post(
                LOGIN_ENDPOINT,
                json={
                    "email": email,
                    "password": password
                }
            )

        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert "email or password are incorrect" in response_data['message']