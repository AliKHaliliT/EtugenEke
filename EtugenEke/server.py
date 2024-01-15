from fastapi import FastAPI
import os
from .assets.utils.get_machine_ip import NetworkConfigFetcher
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from .assets.routes.root import signup as root_signup
from .assets.routes.admin import signup as admin_signup
from .assets.routes.admin.admin_auth import AdminAuth
from .assets.database.db.etugeneke_db import engine
from .assets.routes.admin.admin_panel import Users, LamenessDetection, LamenessDetectionVideos, Services, Plans, Admins
from .assets.routes.actions import signup, transaction, login, delete_account, forgot_password, reset_password, \
                                   inference, update_user_credentials, send_user_lameness_detection_data, update_credit, update_recharged, \
                                   upload_video
from .assets.routes.pages import user_action, password_reset
from .assets.routes.data import plans, services, user_lameness_detection_data, user_info


app = FastAPI()


# If logs folder does not exist, create it
if not os.path.exists("logs"):
    os.makedirs("logs")


# For demo purposes
@app.get("/url_list")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list


# Allow requests from the machine during development
ncf = NetworkConfigFetcher()
origins = []

for interface in ncf.fetch_network_config():
    if interface["Interface"] == "Ethernet" or interface["Interface"] == "eth0":
        origins = [
            f"http://{interface['Address']}:8000",
        ]
        break


@app.middleware("http")
async def x_content_type_options(request, call_next):

    """
    
    This middleware adds the X-Content-Type-Options header to the response. This header prevents the browser from
    MIME-sniffing a response away from the declared content-type. This reduces exposure to drive-by download attacks
    and sites serving user uploaded content that could be treated as executable or dynamic HTML files.


    Parameters
    ----------
    request: Request
        The request object.

    call_next: function
        The next function to call.

    
    Returns
    -------
    response: Response
        The response object.
    
    """

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify the HTTP methods you want to allow
    allow_headers=["*"],  # You can specify the HTTP headers you want to allow

)


app.mount("/static", StaticFiles(directory=r"EtugenEke\assets\static"), name="static")
authentication_backend = AdminAuth(secret_key="EtugenEke")
admin = Admin(app, engine, authentication_backend=authentication_backend, 
              title="EtugenEke Admin Panel")

# Admin
app.include_router(root_signup.router)
app.include_router(admin_signup.router)
admin.add_view(Users)
admin.add_view(LamenessDetection)
admin.add_view(LamenessDetectionVideos)
admin.add_view(Services)
admin.add_view(Plans)
admin.add_view(Admins)

# Actions
app.include_router(signup.router)
app.include_router(transaction.router)
app.include_router(login.router)
app.include_router(delete_account.router)
app.include_router(forgot_password.router)
app.include_router(reset_password.router)
app.include_router(inference.router)
app.include_router(update_user_credentials.router)
app.include_router(send_user_lameness_detection_data.router)
app.include_router(update_credit.router)
app.include_router(update_recharged.router)
app.include_router(upload_video.router)

# Pages
app.include_router(user_action.router)
app.include_router(password_reset.router)

# Data
app.include_router(plans.router)
app.include_router(services.router)
app.include_router(user_lameness_detection_data.router)
app.include_router(user_info.router)