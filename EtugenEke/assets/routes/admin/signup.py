import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from assets.database.db.etugeneke_db import engine
from assets.models.admin import Admin
from assets.database.models.admins import Admins
from fastapi.responses import JSONResponse, Response
import dns.resolver
import bcrypt
from datetime import datetime


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\admin_signup.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

default_admin = {
    "first_name": "admin",
    "last_name": "admin",
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin",
}

default_admin = Admin(**default_admin)

@router.post("/init_admin/")
async def signup(admin: Admin = default_admin) -> JSONResponse:

    """
    
    This endpoint registers an admin based on provided credentials.


    Parameters
    ----------
    admin : Admin
        A model object containing admin details for registration.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the registration request.
    
    """

    logging.info(f"Received: {admin} as payload")

    try:

        with Session() as session:
            
            # Check if the admin exists based on username or email
            admin_exists = session.query(Admins).filter(
                (Admins.username == admin.username) | (Admins.email == admin.email)
            ).first()

            if admin_exists:
                logging.error(f"Admin {admin.username} already exists")
                return JSONResponse(content={"message": "Admin already exists"}, status_code=400)


            # Check email validity by resolving domain
            domain = admin.email.split('@')[-1]
            dns.resolver.resolve(domain, "MX")


            hashed_password = bcrypt.hashpw(admin.password.encode("utf-8"), bcrypt.gensalt())

            # Create the admin object and add it to the database
            new_admin = Admins(
                date_created=datetime.utcnow(),
                role="admin",
                first_name=admin.first_name,
                last_name=admin.last_name,
                username=admin.username,
                email=admin.email,
                password=hashed_password.decode("utf-8"), 
            )
            session.add(new_admin)

            session.commit()


            logging.info(f"Admin {admin.username} registered successfully")
            return JSONResponse(content={"message": "Admin registered successfully"}, status_code=200)
    except dns.resolver.NXDOMAIN:
        logging.error(f"Admin {admin.username} entered invalid email")
        return JSONResponse(content={"message": "Invalid email"}, status_code=400)
    except Exception as e:
        logging.error(f"Error in signup: {e}", exc_info=True)
        return Response(status_code=500)