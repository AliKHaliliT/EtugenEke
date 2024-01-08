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

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\root_signup.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

default_root = {
    "first_name": "root",
    "last_name": "root",
    "username": "root",
    "email": "root@example.com",
    "password": "root",
}

default_root = Admin(**default_root)

@router.post("/init_root/")
async def signup(root: Admin = default_root) -> JSONResponse:

    """
    
    This endpoint registers a root based on provided credentials.


    Parameters
    ----------
    root : Admin
        A model object containing root details for registration.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the registration request.
    
    """

    logging.info(f"Received: {root} as payload")

    try:

        with Session() as session:
            
            # Check if the root exists based on username or email
            root_exists = session.query(Admins).filter(
                (Admins.username == root.username) | (Admins.email == root.email)
            ).first()

            if root_exists:
                logging.error(f"Root {root.username} already exists")
                return JSONResponse(content={"message": "Root already exists"}, status_code=400)


            # Check email validity by resolving domain
            domain = root.email.split('@')[-1]
            dns.resolver.resolve(domain, "MX")


            hashed_password = bcrypt.hashpw(root.password.encode("utf-8"), bcrypt.gensalt())

            # Create the root object and add it to the database
            new_root = Admins(
                date_created=datetime.utcnow(),
                role="root",
                first_name=root.first_name,
                last_name=root.last_name,
                username=root.username,
                email=root.email,
                password=hashed_password.decode("utf-8"), 
            )
            session.add(new_root)

            session.commit()


            logging.info(f"Root {root.username} registered successfully")
            return JSONResponse(content={"message": "Root registered successfully"}, status_code=200)
    except dns.resolver.NXDOMAIN:
        logging.error(f"Root {root.username} entered invalid email")
        return JSONResponse(content={"message": "Invalid email"}, status_code=400)
    except Exception as e:
        logging.error(f"Error in signup: {e}")
        return Response(status_code=500)