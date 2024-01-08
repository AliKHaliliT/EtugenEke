import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from assets.database.db.etugeneke_db import engine
from assets.models.auth import Auth
from assets.database.models.users import Users
import bcrypt
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\login.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/actions/login/")
async def login(credentials: Auth) -> JSONResponse:

    """
    
    This endpoint checks if a user exists based on provided credentials.


    Parameters
    ----------
    credentials : Auth
        A model object containing username or email and password for authentication.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the Auth request.

    """

    logging.info(f"Received: {credentials} as payload")

    try:

        with Session() as session:

            user = session.query(Users).filter(
                (Users.username == credentials.username_or_email) |
                (Users.email == credentials.username_or_email)
            ).first()

            if user:
                if not bcrypt.checkpw(credentials.password.encode("utf-8"), user.password.encode("utf-8")):
                    logging.warning(f"User {credentials.username_or_email} entered incorrect password")
                    return JSONResponse(content={"message": "Incorrect password"}, status_code=401)
                else:
                    logging.info(f"User {credentials.username_or_email} logged in successfully")
                    return JSONResponse(content={"message": "Authentication successful!"}, status_code=200)
            else:
                logging.warning(f"User {credentials.username_or_email} does not exist")
                return JSONResponse(content={"message": "User does not exist"}, status_code=404)
    except Exception as e:
        logging.error(f"Error in Auth: {e}", exc_info=True)
        return Response(status_code=500)