import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.reset_password import ResetPassword
from fastapi.responses import JSONResponse, Response
import bcrypt
from ...database.models.users import Users


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\reset_password.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.patch("/actions/reset_password/")
async def reset_password(request: ResetPassword) -> JSONResponse:

    """
    
    This endpoint resets a user's password based on provided credentials.


    Parameters
    ----------
    request : ResetPassword
        A model object containing token and new password for authentication.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the password reset request.
    
    """

    logging.info(f"Received: {request} as payload")

    try:

        with Session() as session:

            # Check if the token exists and fetch the user
            user = session.query(Users).filter(Users.token == request.token).first()

            if not user:
                logging.error("Token not found")
                return JSONResponse(content={"message": "Token not found"}, status_code=404)

            # Check password and Update the password and token

            if bcrypt.checkpw(request.new_password.encode("utf-8"), user.password.encode("utf-8")):
                logging.error("New password cannot be the same as the old password")
                return JSONResponse(content={"message": "New password cannot be the same as the old password"}, status_code=400)
            
            user.password = bcrypt.hashpw(request.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")  # Update the password in the model

            user.token = ''  # Invalidate the token after password reset

            session.commit()


            logging.info(f"User {user.username} reset their password")
            return JSONResponse(content={"message": "Password reset successfully"}, status_code=200)
    except Exception as e:
        logging.error(f"Error in resetting password: {e}", exc_info=True)
        return Response(status_code=500)