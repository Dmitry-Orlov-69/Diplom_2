import random
import string
import requests
from urls import INGREDIENTS_ENDPOINT

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + '@yandex.ru'

def random_name():
    return ''.join(random.choices(string.ascii_letters, k=8))

def get_ingredients(token):
    ingredients_response = requests.get(
        INGREDIENTS_ENDPOINT,
        headers={'Authorization': f'Token {token}'}
    )
    return ingredients_response.json()