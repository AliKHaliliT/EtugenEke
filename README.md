# EtugenEke

<div align="center" style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;">
  <img src="https://img.shields.io/github/license/AliKHaliliT/EtugenEke" alt="License">
  <img src="https://img.shields.io/github/last-commit/AliKHaliliT/EtugenEke" alt="Last Commit">
  <img src="https://img.shields.io/github/issues/AliKHaliliT/EtugenEke" alt="Open Issues">
</div>

<br/>

<div align="center">
  <img src="https://github.com/AliKHaliliT/EtugenEke/raw/main/util_resources/readme/logo.jpeg?raw=true" alt="EtugenEkeLogo" style="width:300px;height:300px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
</div>

<br/>

> **EtugenEke** is a modern, secure, and modular backend server built using **FastAPI**, designed as a core component of my master's thesis. It powers the companion mobile application [AkAna](https://github.com/AliKHaliliT/AkAna), enabling user authentication, data management, media uploads, and inference workflows.

The logo was generated using [Leonardo.AI](https://leonardo.ai) and enhanced via [Upscale.media](https://upscale.media) for high-resolution clarity.

---

## 🌟 Overview

EtugenEke serves as a full-featured RESTful API with support for authentication, file handling, admin controls, and dynamic content delivery. It emphasizes clean architecture, scalability, and extensibility, ideal for integration with frontend or mobile clients.

Key features include:
- 🔐 Secure password reset with tokenized deep linking
- 📱 DeepLink redirection based on device type (mobile app ↔ web)
- 📁 File and video upload handling
- 👨‍💼 Admin interface for data management
- 🧪 Modular design with documented endpoints
- 📦 Built-in logging and configuration utilities

---

## 🛠️ Tech Stack

This project leverages modern Python tools and frameworks:

| Component              | Technology Used                                                                 |
|------------------------|----------------------------------------------------------------------------------|
| **Web Framework**       | [FastAPI](https://fastapi.tiangolo.com/) – High-performance API framework        |
| **ASGI Server**         | [Uvicorn](https://www.uvicorn.org/) – Lightning-fast ASGI server                  |
| **Database ORM**        | [SQLAlchemy](https://www.sqlalchemy.org/) – SQL toolkit and ORM                   |
| **Database**            | SQLite (lightweight, file-based; easily replaceable with PostgreSQL in prod)     |
| **Data Validation**     | [Pydantic](https://pydantic-docs.helpmanual.io/) – Type hints & runtime validation|
| **Admin Panel**         | [SQLAdmin](https://github.com/aminalaee/sqladmin) – Elegant admin UI              |
| **File Storage**        | [FastAPI-Storages](https://github.com/aminalaee/fastapi-storages) – Async storage support |
| **Password Hashing**    | `bcrypt` – Secure hashing for user credentials                                   |
| **Token Generation**    | Python’s `secrets` module – Cryptographically secure tokens                      |
| **Logging**             | Python `logging` module – Structured log output stored in `/logs` directory      |

---

## 🔐 Authentication & Security

### Password Reset Flow
A secure token-based password reset system is implemented:
1. User requests reset via `/actions/forgot_password/`.
2. A unique, one-time-use token is generated using `secrets.token_urlsafe()`.
3. A link containing the token is sent to the user’s email.
4. Clicking the link triggers `/pages/user_action`, which:
   - Detects device type (mobile/desktop)
   - Redirects mobile users to the [AkAna](https://github.com/AliKHaliliT/AkAna) app via **DeepLinking**
   - Sends desktop users to `/pages/password_reset` for web-based reset

> ⚠️ **Note**: In this development version, tokens are invalidated only after use. For production, time-based expiration (e.g., 1-hour TTL) and rate-limiting should be added.

> ⚠️ **Note**: Since this is a development-level, thesis-oriented implementation, many enterprise-grade features were intentionally simplified to facilitate faster and easier academic development. Features such as a proper project structure, dependency injection, robust database handling, configuration management, logging, security practices, request validation, error handling, and other production-scale concerns were minimized or omitted. In a production-ready FastAPI or any backend system, these components are essential for maintainability, scalability, and reliability.

<div align="center">
  <img src="https://github.com/AliKHaliliT/EtugenEke/raw/main/util_resources/readme/reset_password_func.gif?raw=true" alt="Password Reset Flow Demo" style="max-width:100%; border: 1px solid #ddd; border-radius: 8px;">
</div>

> 🔒 Sensitive data such as passwords are hashed using `bcrypt`. However, authentication headers (e.g., Bearer tokens) are not yet implemented and the credentials are passed in request bodies. This is suitable for development but **should be upgraded for production use**.

---

## 🖼️ Admin Panel

Manage users, services, plans, and more through an intuitive admin dashboard powered by SQLAdmin.

To access:
1. Run the server.
2. Create an admin user:
   ```bash
   python init_admin.py
   ```
   > Credentials: `admin` / `admin`

3. Access at: `http://localhost:8000/admin`

For full administrative privileges (including editing other admins), create a root user:
```bash
python init_root.py
```
> Credentials: `root` / `root`

<div align="center">
  <img src="https://github.com/AliKHaliliT/EtugenEke/raw/main/util_resources/readme/admin_panel.png?raw=true" alt="Admin Panel Screenshot" style="max-width:100%; border: 1px solid #ddd; border-radius: 8px; margin-top: 1rem;">
</div>

---

## 🚀 Installation

### Prerequisites
- Python 3.12+
- `pip`

### Clone & Setup
```bash
git clone https://github.com/AliKHaliliT/EtugenEke
cd EtugenEke
```

Install dependencies:
```bash
pip install -r requirements.txt
```

If dependency resolution fails:
```bash
pip install -r requirements_env.txt
```

---

## ▶️ Usage

### Start the Development Server
```bash
uvicorn EtugenEke:app --reload
```
Visit the API at: `http://localhost:8000`

### Network Broadcast Mode (for local testing across devices)
```bash
uvicorn EtugenEke:app --reload --host 0.0.0.0 --port 8000
```
Other devices on the same network can access the server using your machine’s IP address.

> 💡 The script `EtugenEke/assets/utils/get_machine_ip.py` automatically detects and sets the appropriate local IP. If the server is unresponsive, manually set the IP in this file. Supports both Windows and Linux.

> ⏳ A slight delay during startup/reload is expected due to background IP detection.

---

## 🧪 Testing Endpoints

After starting the server, seed required data via the admin panel (`/admin`):
- Add at least one **Plan**
- Add one **Service** (you can use sample images from `data/services/`)

### Test User Flow (Signup, Login, Forgot Password)
Run this script to test core actions:

```python
import requests

BASE_URL = "http://localhost:8000"
BASE_URL_ACTIONS = f"{BASE_URL}/actions"
BASE_URL_PAGES = f"{BASE_URL}/pages"

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
    print("Signup:", response.json())

def test_login():
    response = requests.post(f"{BASE_URL_ACTIONS}/login/", json=login_data)
    print("Login:", response.json())

def test_forgot_password():
    response = requests.post(f"{BASE_URL_ACTIONS}/forgot_password/", json=forgot_password_data)
    print("Forgot Password:", response.json())

test_signup()
test_login()
test_forgot_password()
```

### Test Video Upload & Inference
Upload a video for processing:

```python
import requests

url = "http://127.0.0.1:8000/actions/inference/"
credentials = {
    "username_or_email": "canislupus",
    "password": "canis",
    "service_type": "Lameness Detection"
}
files = {'file': open('util_resources/samples/video/test_video.mp4', 'rb')}

response = requests.post(url, data=credentials, files=files)
print(response.text)
```

Uploaded files are stored in the `uploads/` directory.

---

## 🗂️ Project Structure

### Key Endpoints

| Purpose                            | Endpoint                                 |
|------------------------------------|-------------------------------------------|
| Static Files                       | `/static`                                 |
| Admin Panel                        | `/admin`                                  |
| Initialize Root User               | `/init_root/`                             |
| Initialize Admin User              | `/init_admin/`                            |
| User Signup                        | `/actions/signup/`                        |
| User Login                         | `/actions/login/`                         |
| Delete Account                     | `/actions/delete_account/`                |
| Forgot Password                    | `/actions/forgot_password/`               |
| Reset Password                     | `/actions/reset_password/`                |
| Inference (Video Upload)           | `/actions/inference/`                     |
| Update User Credentials            | `/actions/update_user_credentials/`       |
| Send Lameness Detection Data       | `/actions/send_user_lameness_detection_data/` |
| Update Credit                      | `/actions/update_credit/`                 |
| Mark Recharged                     | `/actions/update_recharged/`              |
| Upload Video                       | `/actions/upload_video/`                  |
| Redirect Handler (DeepLink)        | `/pages/user_action`                      |
| Password Reset Page                | `/pages/password_reset`                   |
| Get Available Plans                | `/data/plans/`                            |
| Get Services by Plan               | `/data/services/`                         |
| Get User Lameness Data             | `/data/user_lameness_detection_data/`     |
| Get User Info                      | `/data/user_info/`                        |

All endpoints are documented via FastAPI’s auto-generated OpenAPI/Swagger UI at:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs) or [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📖 About

In Turkic mythology, **Etugen Eke** (also spelled *Etügen Eke*) roughly translates to *"Brown Skinned Mother Earth"*. She is revered as the sacred spirit of the earth, fertility, and nature, often associated with Ötüken (the holy mountain of the earth and fertility), the spiritual center of the ancient Turkic world.

📚 Learn more: [Etugen Eke on Wikipedia](https://en.wikipedia.org/wiki/Etugen_Eke)

---

## 🔗 Frontend

The frontend companion app lives in the sister repository, [AkAna](https://github.com/AliKHaliliT/AkAna).

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.