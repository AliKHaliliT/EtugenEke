import requests


BASE_URL = "http://localhost:8000"
BASE_URL_ACTIONS = f"{BASE_URL}/actions"
BASE_URL_PAGES = f"{BASE_URL}/pages"
BASE_URL_ASSETS = f"{BASE_URL}/assets"
BASE_URL_DATA = f"{BASE_URL}/data"


signup_data = {
    "first_name": "Canis",
    "last_name": "Canis",
    "username": "canislupus",
    "email": "canis.lupus@example.com",
    "password": "canis",
    "plan": "Free",
}

login_data = {
    "username_or_email": "canislupus",
    "password": "secretpassword"
}

forgot_password_data = {
    "username_or_email": "canislupus"
}


def test_signup():
    response = requests.post(f"{BASE_URL_ACTIONS}/signup/", json=signup_data)
    print(response.json())

def test_login():
    response = requests.post(f"{BASE_URL_ACTIONS}/login/", json=login_data)
    print(response.json())

def test_forgot_password():
    response = requests.post(f"{BASE_URL_ACTIONS}/forgot_password/", json=forgot_password_data)
    print(response.json())


test_signup()

test_login()

test_forgot_password()