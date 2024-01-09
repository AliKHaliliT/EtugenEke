import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.auth import Auth
from ...models.update_credit import UpdateCredit
from fastapi.responses import JSONResponse, Response
from ...database.models.users import Users
import bcrypt


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\update_credit.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.patch("/actions/update_credit/")
async def update_credit(user: Auth, credit: UpdateCredit) -> JSONResponse:

    """

    This endpoint updates user's credit based on provided credentials and the value of the credit to be changed.

    
    Parameters
    ----------
    user : Auth
        A model object containing the user credentials for authentication.

    credit : UpdateCredit
        A model object containing the credit value to be changed.

        
    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the user credit update.

    """

    logging.info(f"Received: {user} and {credit} as payload")
    
    try:

        with Session() as session:

            # Fetch user by username
            user_exists = session.query(Users).filter(Users.username == user.username_or_email).first()

            if user_exists:
                if not bcrypt.checkpw(user.password.encode("utf-8"), user_exists.password.encode("utf-8")):
                    logging.error("Incorrect password")
                    return JSONResponse(content={"message": "Incorrect password"}, status_code=401)
            else:
                logging.error("User does not exist")
                return JSONResponse(content={"message": "User does not exist"}, status_code=404)
            
            # Update user's credit
            user_exists.credit = user_exists.credit - (user_exists.credit - credit.credit)

            session.commit()


            logging.info(f"{user_exists.username}'s credit updated successfully")
            return JSONResponse(content={"message": "User's credit updated successfully"}, status_code=200)
    except Exception as e:
        logging.error(f"Error in updating user's credit: {e}", exc_info=True)
        return Response(status_code=500)