# EtugenEke

<p align="center">
  <img src="readme_assets\logo.jpeg" alt="EtugenEkeLogo" style="width:300px;height:300px;">
</p>

A Server built using FastAPI for a part of my thesis.

The logo was created using [LeonardoAI](https://leonardo.ai). It was then polished and enhanced with [UpscaleMedia](https://upscale.media).

### Components
- The core is built using [FastAPI](https://fastapi.tiangolo.com/).
- The database is SQLite, which is managed using [SQLAlchemy](https://www.sqlalchemy.org/).
- The server is deployed using [Uvicorn](https://www.uvicorn.org/).
- The storage is managed using [FastAPI Storages](https://github.com/aminalaee/fastapi-storages).
- The admin panel is built using [SQLAlchemy Admin](https://github.com/aminalaee/sqladmin).
- Data is validated using [Pydantic](https://pydantic-docs.helpmanual.io/).

The server contains unique token generation for password reset. Given a valid request is made to the `/actions/forgot_password/` endpoint, a token is generated and sent to the user's email. The token is then used to verify the user's identity when they get redirected to the `/pages/password_reset` endpoint by clicking the link in the email and opening the `/pages/user_action` endpoint. The `/pages/user_action` endpoint is also used to choose where to redirect the user based on the device they are using. If the user is on a mobile device, and has the coprrespounding app, [AkAna](https://github.com/AliKHaliliT/AkAna), installed, they will get redirected to the app using the DeepLinking Mechanism, and if they are on a desktop, they are redirected to the `/pages/password_reset` endpoint which contains a form to reset the password. The token is generated using python's `secrets` module. No time-based invalidation is used, instead, the token is invalidated once it is used to reset the password. So on a production server, the token should be invalidated after a certain amount of time. Also, other proper security measures should be taken into consideration instead of the one curretly used as this is just a simple dummy implementation.

The user action page and the password reset page look like the following:
<iframe src="EtugenEke\assets\static\content\userAction.html">

All of the endpoints are documented which explains their functionality and the expected input and output.

The server contains the following endpoints:

- static
  - /static
- admin
  - /admin
- signup
  - /init_root/
- signup
  - /init_admin/
- signup
  - /actions/signup/
- transaction
  - /actions/transaction/
- login
  - /actions/login/
- delete_account
  - /actions/delete_account/
- forgot_password
  - /actions/forgot_password/
- reset_password
  - /actions/reset_password/
- upload_video
  - /actions/inference/
- update_user_credentials
  - /actions/update_user_credentials/
- send_user_lameness_detection_data
  - /actions/send_user_lameness_detection_data/
- update_credit
  - /actions/update_credit/
- update_recharged
  - /actions/update_recharged/
- upload_video
  - /actions/upload_video/
- user_action
  - /pages/user_action
- password_reset
  - /pages/password_reset
- plans
  - /data/plans/
- services
  - /data/services/
- user_lameness_detection_data
  - /data/user_lameness_detection_data/
- user_info
  - /data/user_info/


## License
This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.