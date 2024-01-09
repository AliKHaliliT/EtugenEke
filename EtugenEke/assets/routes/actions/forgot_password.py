import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.forgot_password import ForgotPassword
from ...database.models.users import Users
from ...utils.generate_reset_token import generate
from ...utils.send_reset_mail import send
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\forgot_password.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/actions/forgot_password/")
async def forgot_password(request: ForgotPassword) -> JSONResponse:

    """

    This endpoint checks if a user exists based on provided credentials and 
    updates the user's token for password reset then sends a reset link to
    the user's email.


    Parameters
    ----------
    request : ForgotPassword
        A model object containing username or email for authentication.

    
    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the password reset request.

    """

    logging.info(f"Received: {request} as payload")

    try:

        with Session() as session:

            # Fetch user by username or email
            user = session.query(Users).filter(
                (Users.username == request.username_or_email) | (Users.email == request.username_or_email)
            ).first()

            if user:
                # Generate a reset token and send it to the user's email
                reset_token = generate()
                send(user.email, reset_token)

                # Update the user's token for password reset
                user.token = reset_token
                
                session.commit()


                logging.info(f"User {request.username_or_email} requested password reset")
                return JSONResponse(content={"message": "User exists. The password reset link has been sent to the user's email."}, status_code=200)
            else:
                logging.warning(f"User {request.username_or_email} does not exist")
                return JSONResponse(content={"message": "User does not exist"}, status_code=404)
    except Exception as e:
        logging.error(f"Error in forgot password: {e}", exc_info=True)
        return Response(status_code=500)