# EtugenEke
<div align="center">
  <img src="readme_assets\img\logo.jpeg" alt="EtugenEkeLogo" style="width:300px;height:300px;">
</div>

A Server built using FastAPI for a part of my thesis.

The logo was created using [LeonardoAI](https://leonardo.ai). It was then polished and enhanced with [UpscaleMedia](https://upscale.media).

### Components
- The core is built using [FastAPI](https://fastapi.tiangolo.com/).
- The database is SQLite, which is managed using [SQLAlchemy](https://www.sqlalchemy.org/).
- The server is deployed using [Uvicorn](https://www.uvicorn.org/).
- The storage is managed using [FastAPI Storages](https://github.com/aminalaee/fastapi-storages).
- The admin panel is built using [SQLAlchemy Admin](https://github.com/aminalaee/sqladmin).
- Data is validated using [Pydantic](https://pydantic-docs.helpmanual.io/).

The servers uses Python's [logging](https://docs.python.org/3/library/logging.html) module for logging. The logs are stored in the `logs` folder.

The server contains unique token generation for password reset. Given a valid request is made to the `/actions/forgot_password/` endpoint, a token is generated and sent to the user's email. The token is then used to verify the user's identity when they get redirected to the `/pages/password_reset` endpoint by clicking the link in the email and opening the `/pages/user_action` endpoint. The `/pages/user_action` endpoint is also used to choose where to redirect the user based on the device they are using. If the user is on a mobile device, and has the coprrespounding app, [AkAna](https://github.com/AliKHaliliT/AkAna), installed, they will get redirected to the app using the DeepLinking Mechanism, and if they are on a desktop, they are redirected to the `/pages/password_reset` endpoint which contains a form to reset the password. The token is generated using python's `secrets` module. No time-based invalidation is used, instead, the token is invalidated once it is used to reset the password. So on a production scenario, the token should be invalidated after a certain amount of time. Also, other proper security measures should be taken into consideration instead of the one curretly used as this is just a simple dummy implementation.

The reset password functionality on the desktop looks like below:
<div align="center">
  <img src="readme_assets\img\reset_password_func.gif" alt="passwordResetFunc.gif">
</div>

The sensitive information like passwords are hashed using [bcrypt](https://pypi.org/project/bcrypt/). However, the use of authentication headers is not implemented. Instead, the user's email and password are sent in the body of the request. In a production scenario, the use of authentication headers should be considered.

The code base is modularized and all of the endpoints are documented.

## Installation

The server is developed using `python==3.12.0`.

To run the server, first install the dependencies using the following command:
```bash
pip install -r requirements.txt

```

In case the above command fails to install the required dependencies, you can try installing the dependencies of the whole environment using the following command:

```bash
pip install -r requirements_env.txt

```
## Usage
Then, run the following command:
```bash
uvicorn EtugenEke:app --reload
```
The server will be running on `http://localhost:8000`.

In order to broadcast the server to the local network, run the following command:
```bash
uvicorn EtugenEke:app --reload --host 0.0.0.0 --port 8000
```

When running the server on the broadcast mode on a local network, the server can be accessed from other devices on the network using the IP address of the device running the server and the port number. To facilitate the process of setting the IP address of the device running the server, on the server side, the `EtugenEke\assets\utils\get_machine_ip.py` automatically sets the most suitable IP address for the server. However, if the server is unresponsive, you might need to manually set the IP address of the device running the server in the `EtugenEke\assets\utils\get_machine_ip.py` file to statically reflect the IP address of the device running the server. The script supports both linux and windows. The slight delay on server start and reload is due to the script running on the background to set the IP address of the device running the server.

### Superuser

To access the admin panel, you need to create a superuser. To do so, run the sever and then run the following command which will create an admin user with credentials:
```
username: admin
password: admin
```
 that can access the admin panel:
```bash
python init_admin.py
```
Then, you can access the admin panel on `http://localhost:8000/admin`.

The admin has access to everything but can not view or edit himself or other admins. You can use the following command to create a root user with the following credentials:
```
username: root
password: root
```
that can view and edit admins:
```bash
python init_root.py
```
The admin panel will look like below:
<div align="center">
  <img src="readme_assets\img\admin_panel.png" alt="adminPanel.png">
</div>

### Test Endpoints
In order to use the server, you must first define some data. It does not matter what you define as long as it is in the correct format. Thus, after accessing the admin panel, create atleast a plan and a service. You can use the image in the `data\services` for the service image. Then, you can use the following python script to test the sign-up, login and forgot password endpoints:
```python
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
    "password": "canis"
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
```

The srever also supports video upload. To test the video upload functionality, you can use the following python script:
```python
import requests


url = "http://localhost:8000/actions/inference/"


credentials = {
    "username_or_email": "canislupus",
    "password": "canis",
    "service_type": "the_service_type_that_you_defined_in_the_admin_panel",
}

files = {'file': open(r'util_resources\video\test_video.mp4', 'rb')}


response = requests.post(url, data=credentials, files=files)


print(response.text)
```
The uploaded file will be available in the `uploads` folder.

## Structure
The server contains the following endpoints:

- Static files
  - /static
- Admin panel
  - /admin
- Signup a root user
  - /init_root/
- Signup an admin user
  - /init_admin/
- Signup a user
  - /actions/signup/
- Transaction
  - /actions/transaction/
- Login
  - /actions/login/
- Delete account
  - /actions/delete_account/
- Forgot password
  - /actions/forgot_password/
- Reset password
  - /actions/reset_password/
- Inference
  - /actions/inference/
- Update user credentials
  - /actions/update_user_credentials/
- Send user lameness detection data
  - /actions/send_user_lameness_detection_data/
- Update credit
  - /actions/update_credit/
- Update recharged column for a user
  - /actions/update_recharged/
- Upload a video to the server for a user
  - /actions/upload_video/
- Helper redirect endpoint
  - /pages/user_action
- Password reset page
  - /pages/password_reset
- Serve available plans to purchase
  - /data/plans/
- Get available services for a plan and a user
  - /data/services/
- Get user lameness detection data
  - /data/user_lameness_detection_data/
- Get user info
  - /data/user_info/

## About
I developed this server as a component of my master's thesis. The server is intended for a mobile app called AkAna.
Regarding its name, In my native language, "Eke" means mother, while Etugen is also often referred to as "dayir" (meaning brown), and she is described as the Brown Skinned Mother Earth. Also her name may have originated from Ötüken, the holy mountain of the earth and fertility. Etugen existed in the middle of the Universe and the Turkic people viewed Etugen as the second highest deity ([From Wikipedia](https://en.wikipedia.org/wiki/Etugen_Eke)).

## Frontend
The frontend lives in the sister repository [AkAna](https://github.com/AliKHaliliT/AkAna).

## License
This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.