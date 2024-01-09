import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.auth import Auth
from ...routes.actions.login import login
from fastapi.responses import JSONResponse, Response
from ...database.models.users import Users


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'logs\delete_account.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.delete("/actions/delete_account/")
async def delete_account(credentials: Auth) -> JSONResponse:

    """

    This endpoint deletes a user account based on provided credentials.

    
    Parameters
    ----------
    credentials : Auth
        A model object containing username and password for authentication.

        
    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the account deletion request.

    """

    logging.info(f"Received: {credentials} as payload")

    try:
        # Authenticate user
        login_response = await login(credentials)

        if login_response.status_code == 200:

            with Session() as session:

                # Fetch user by username
                user = session.query(Users).filter(Users.username == credentials.username_or_email).first()

                if user:
                    # Delete the user
                    session.delete(user)

                    session.commit()


                    logging.info(f"User {credentials.username_or_email} deleted their account")
                    return JSONResponse(content={"message": "Account deleted successfully"}, status_code=200)
                else:
                    logging.warning(f"User {credentials.username_or_email} does not exist")
                    return JSONResponse(content={"message": "User not found"}, status_code=404)
        else:
            logging.warning(f"User {credentials.username_or_email} failed to authenticate")
            return JSONResponse(content={"message": "Authentication failed"}, status_code=401)
    except Exception as e:
        logging.error(f"Error in deleting account: {e}", exc_info=True)
        return Response(status_code=500)