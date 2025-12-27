import requests
import allure
from urls import INGREDIENTS_ENDPOINT, LOGIN_ENDPOINT, ORDERS_ENDPOINT
from helpers import get_ingredients

class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_authorization(self, unique_user):
        with allure.step("Получение токена авторизации"):
            email = unique_user['user_data']['email']
            password = unique_user['user_data']['password']
            response = requests.post(
                LOGIN_ENDPOINT,
                json={
                    "email": email,
                    "password": password
                }
            )
            token = response.json()['accessToken']

        with allure.step("Запрос данных об ингредиентах"):
            ingredients = get_ingredients(token)

        with allure.step("Создание заказа"):
            order_data = {
                "ingredients": [ingredients['data'][0]['_id'], ingredients['data'][1]['_id']],
            }

            response = requests.post(
                ORDERS_ENDPOINT,
                json=order_data,
                headers={'Authorization': f'Token {token}'}
            )

            order = response.json()
            assert response.status_code == 200
            assert 'order' in order

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self):
        with allure.step("Запрос данных об ингредиентах без авторизации"):
            ingredients_response = requests.get(
                INGREDIENTS_ENDPOINT
            )
            assert ingredients_response.status_code == 200
            ingredients = ingredients_response.json()

        with allure.step("Попытка создать заказ без предоставления токена авторизации"):
            order_data = {
                "ingredients": [ingredients['data'][0]['_id'], ingredients['data'][1]['_id']],
            }
            response = requests.post(
                ORDERS_ENDPOINT,
                json=order_data
            )

            assert response.status_code != 200  # Ожидается, что создание заказа без авторизации не пройдет успешно
    
    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, unique_user):
        with allure.step("Получение токена авторизации"):
            email = unique_user['user_data']['email']
            password = unique_user['user_data']['password']
            response = requests.post(
                LOGIN_ENDPOINT,
                json={
                    "email": email,
                    "password": password
                }
            )
            token = response.json()['accessToken']

        with allure.step("Запрос данных об ингредиентах"):
            ingredients = get_ingredients(token)

        with allure.step("Создание заказа"):
            order_data = {
                "ingredients": [ingredients['data'][0]['_id'], ingredients['data'][1]['_id']],
            }

            response = requests.post(
                ORDERS_ENDPOINT,
                json=order_data,
                headers={'Authorization': f'Token {token}'}
            )

            order = response.json()
            assert response.status_code == 200
            assert 'order' in order

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, unique_user):
        with allure.step("Получение токена авторизации"):
            email = unique_user['user_data']['email']
            password = unique_user['user_data']['password']
            response = requests.post(
                LOGIN_ENDPOINT,
                json={
                    "email": email,
                    "password": password
                }
            )
            assert response.status_code == 200
            token = response.json()['accessToken']

        with allure.step("Попытка создать заказ без ингредиентов"):
            order_data = {}
            response = requests.post(
                ORDERS_ENDPOINT,
                json=order_data,
                headers={'Authorization': f'Token {token}'}
            )

            assert response.status_code == 400  # Ожидается, что создание заказа без ингредиентов вернёт код 400

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, unique_user):
        with allure.step("Получение токена авторизации"):
            email = unique_user['user_data']['email']
            password = unique_user['user_data']['password']
            response = requests.post(
                LOGIN_ENDPOINT,
                json={
                    "email": email,
                    "password": password
                }
            )
            assert response.status_code == 200
            token = response.json()['accessToken']

        with allure.step("Попытка создать заказ с неверным хешем ингредиента"):
            order_data = {
                "ingredients": ["invalid_hash"]
            }
            response = requests.post(
                ORDERS_ENDPOINT,
                json=order_data,
                headers={'Authorization': f'Token {token}'}
            )

            assert response.status_code == 500  # Ожидается, что создание заказа с неверным хешем вернёт код 500