from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
import logging
from assets.database.db.etugeneke_db import engine
from assets.models.auth import Auth
from assets.database.models.users import Users
import bcrypt
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\user_info.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/data/user_info/")
async def user_info(credentials: Auth) -> JSONResponse:

    """
    
    This endpoint fetches the user information. It returns the user information in a JSON format which containes the
    user's firstname, lastname, username, email, subscription plan and the number of credits left.


    Parameters
    ----------
    credentials : Auth
        A model object containing user credentials for retrieving info.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the user info retrieval request and the user info if successful.
    
    """

    logging.info(f"Received: {credentials} as payload")
    
    try:

        with Session() as session:

            # Fetch user by username or email
            user = session.query(Users).filter(
                (Users.username == credentials.username_or_email) | (Users.email == credentials.username_or_email)
            ).first()

            if user:
                if not bcrypt.checkpw(credentials.password.encode("utf-8"), user.password.encode("utf-8")):
                    logging.error("Incorrect password")
                    return JSONResponse(content={"message": "Incorrect password"}, status_code=401)
            else:
                logging.error("User does not exist")
                return JSONResponse(content={"message": "User does not exist"}, status_code=404)
            
            # Organize fetched database entries into a dictionary with dates as keys
            data_dict = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "plan": user.plan,
                "credit": user.credit,
                "recharged": user.recharged
            }


            logging.info(f"User {user.username} found")
            return JSONResponse(content={"message": "User found", "data": data_dict}, status_code=200)
    except Exception as e:
        logging.error(f"Error in retrieving user info: {e}", exc_info=True)
        return Response(status_code=500)