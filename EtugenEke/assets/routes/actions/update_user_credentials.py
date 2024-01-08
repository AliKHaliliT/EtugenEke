import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from assets.database.db.etugeneke_db import engine
from assets.models.auth import Auth
from fastapi.responses import JSONResponse, Response
from assets.database.models.users import Users
import bcrypt


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\update_user_credentials.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.patch("/actions/update_user_credentials/")
async def update_user_credentials(user: Auth, actions: dict[str, str]) -> JSONResponse:

    """

    This endpoint updates user details based on provided credentials.

    
    Parameters
    ----------
    user : Auth
        A model object containing the current user credentials for authentication.

    actions : dict
        A dictionary containing the actions to perform on the user details.
        Each key is a string containing the name of the action and each value is a string containing the new value
        for the detail.

        
    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the user details update.

    """

    if not isinstance(actions, dict):
        logging.error("actions must be a dictionary")
        return JSONResponse(content={"message": "actions must be a dictionary"}, status_code=400)
    for action, new_info in actions.items():
        if not isinstance(action, str):
            logging.error("Invalid action. Action must be a string.")
            return JSONResponse(content={"message": "Invalid action. Action must be a string."}, status_code=400)
        if not isinstance(new_info, str):
            logging.error("Invalid new info. The new info must be a string.")
            return JSONResponse(content={"message": "Invalid new info. The new info must be a string."}, status_code=400)

    logging.info(f"Received: {user} as payload")
    
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
            
            # Update user details
            for action, new_info in actions.items():
                if action == "update_first_name":
                    user_exists.first_name = new_info
                elif action == "update_last_name":
                    user_exists.last_name = new_info
                elif action == "update_username":
                    user_exists.username = new_info
                elif action == "update_email":
                    user_exists.email = new_info
                elif action == "update_password":
                    hashed_password = bcrypt.hashpw(new_info.encode("utf-8"), bcrypt.gensalt())
                    user_exists.password = hashed_password.decode("utf-8")


            session.commit()


            logging.info(f"User {user.username_or_email} updated their details")
            return JSONResponse(content={"message": "User details updated successfully"}, status_code=200)
    except Exception as e:
        logging.error(f"Error in updating user details: {e}", exc_info=True)
        return Response(status_code=500)