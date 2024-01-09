import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.forgot_password import ForgotPassword
from fastapi.responses import JSONResponse, Response
from ...database.models.users import Users
import bcrypt


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'logs\update_recharged.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.patch("/actions/update_recharged/")
async def update_recharged(username_or_email: ForgotPassword) -> JSONResponse:

    """

    This endpoint updates user's recharged status based on provided credentials.

    
    Parameters
    ----------
    username_or_email : ForgotPassword
        A model object containing user's username or email for updating recharged status.

        
    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the user's recharged status update.

    """

    logging.info(f"Received: {username_or_email} as payload")
    
    try:

        with Session() as session:

            # Fetch user by username
            user_exists = session.query(Users).filter(Users.username == username_or_email.username_or_email).first()

            if not user_exists:
                logging.warning(f"User {username_or_email.username_or_email} does not exist")
                return JSONResponse(content={"message": "User does not exist"}, status_code=404)
            
            # Update user's recharged status
            user_exists.recharged = False

            session.commit()


            logging.info(f"{user_exists.username}'s recharged updated successfully")
            return JSONResponse(content={"message": "User's recharged updated successfully"}, status_code=200)
    except Exception as e:
        logging.error(f"Error in updating user's recharged: {e}", exc_info=True)
        return Response(status_code=500)