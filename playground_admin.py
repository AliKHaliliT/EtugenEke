import requests


BASE_URL = "http://127.0.0.1:8000"
BASE_URL_ACTIONS = f"{BASE_URL}/actions"
BASE_URL_PAGES = f"{BASE_URL}/pages"
BASE_URL_ASSETS = f"{BASE_URL}/assets"
BASE_URL_DATA = f"{BASE_URL}/data"


def test_transaction():
    response = requests.get(f"{BASE_URL_ACTIONS}/transaction/")
    print(response.json())

def test_plans():
    response = requests.get(f"{BASE_URL_DATA}/plans/")
    print(response.json())


test_transaction()

test_plans()