import requests


BASE_URL = "http://127.0.0.1:8000"
BASE_URL_ACTIONS = f"{BASE_URL}/actions"
BASE_URL_PAGES = f"{BASE_URL}/pages"
BASE_URL_ASSETS = f"{BASE_URL}/assets"
BASE_URL_DATA = f"{BASE_URL}/data"


signup_data = {
    "first_name": "Ali",
    "last_name": "Khalili",
    "username": "alikhalili",
    "email": "ali.khalili.t98@gmail.com",
    "password": "secretpassword",
    "plan": "Free",
}

login_data = {
    "username_or_email": "alikhalili",
    "password": "secretpassword"
}

forgot_password_data = {
    "username_or_email": "alikhalili"
}

new_info = {
    "update_username": "alikhalilidev",
    "update_email": "ali.khalili.t98.dev@gmail.com",
}

update_user_credentials_data = {
    "user": login_data,
    "actions": new_info
}

delete_account_data = {
    "username_or_email": "alikhalilidev",
    "password": "btuh"
}

lameness_detection_data = {
    "username": "alikhalili",
    "date": "Dec 26 2023",
    "healthy": 10,
    "lame": 20,
    "fir": 30,
    "uncertain": 40
}

lameness_detection_data_payload = {
    "credentials": login_data,
    "lameness_detection_data": lameness_detection_data
}

update_credit_data = {
    "credit": 20
}

update_credit_payload = {
    "user": login_data,
    "credit": update_credit_data
}

update_recharged_data = {
    "username_or_email": "alikhalili",
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

def test_update_user_credentials():
    response = requests.patch(f"{BASE_URL_ACTIONS}/update_user_credentials/", json=update_user_credentials_data)
    print(response.json())

def test_delete_account():
    response = requests.delete(f"{BASE_URL_ACTIONS}/delete_account/", json=delete_account_data)
    print(response.json())
    
def test_send_user_lameness_detection_data():
    response = requests.post(f"{BASE_URL_ACTIONS}/send_user_lameness_detection_data/", json=lameness_detection_data_payload)
    print(response.json())

def test_user_lameness_detection_data():
    response = requests.post(f"{BASE_URL_DATA}/user_lameness_detection_data", json=login_data)
    print(response.json())

def test_services():
    response = requests.post(f"{BASE_URL_DATA}/services", json=login_data)
    print(response.json())

def test_user_info():
    response = requests.post(f"{BASE_URL_DATA}/user_info", json=login_data)
    print(response.json())

def test_update_credit():
    response = requests.patch(f"{BASE_URL_ACTIONS}/update_credit/", json=update_credit_payload)
    print(response.json())

def test_update_recharged():
    response = requests.patch(f"{BASE_URL_ACTIONS}/update_recharged/", json=update_recharged_data)
    print(response.json())


test_signup()

# test_login()

test_forgot_password()

# test_update_user_credentials()

# test_delete_account()

# test_send_user_lameness_detection_data()

# test_user_lameness_detection_data()

# test_services()

# test_user_info()

# test_update_credit()

# test_update_recharged()