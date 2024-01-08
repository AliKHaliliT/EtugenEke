import requests


BASE_URL = "http://127.0.0.1:8000"


def test_root_signup():
    response = requests.post(f"{BASE_URL}/init_root/")
    print(response.json())


if __name__ == "__main__":
    test_root_signup()