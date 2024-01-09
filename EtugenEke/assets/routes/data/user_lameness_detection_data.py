import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.auth import Auth
from ...routes.actions.login import login
from ...database.models.lameness_detection_data import LamenessDetectionData
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'logs\user_lameness_detection_data.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/data/user_lameness_detection_data/")
async def user_lameness_detection_data(credentials: Auth) -> JSONResponse:

    """
    
    This endpoint fetches the user data related to lameness detection.
    The data will be served in a JSON format which containes the service type and the number of
    sessions(days, if any) the user has used that service and the details related to that session. 


    Parameters
    ----------
    credentials : Auth
        A model object containing user credentials for retrieving data.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the data retrieval request and the data if successful.
    
    """

    logging.info(f"Received: {credentials} as payload")
    
    try:
        # Authenticate user
        login_response = await login(credentials)

        if login_response.status_code == 200:

            with Session() as session:

                # Fetch user's lameness detection data
                user_data = session.query(LamenessDetectionData).filter(
                    LamenessDetectionData.username == credentials.username_or_email
                ).all()

                if not user_data:
                    logging.error("No data found")
                    return JSONResponse(content={"message": "No data found"}, status_code=404)

                # Organize fetched database entries into a dictionary with dates as keys
                data_dict = {}
                for data_entry in user_data:
                    data_dict[data_entry.date] = {
                        "healthy": data_entry.healthy,
                        "lame": data_entry.lame,
                        "fir": data_entry.fir,
                        "uncertain": data_entry.uncertain
                    }

                # Reverse the order of the dictionary
                data_dict = dict(reversed(list(data_dict.items())))


                logging.info(f"User {credentials.username_or_email} retrieved their lameness detection data")
                return JSONResponse(content={"message": "Data found", "data": data_dict}, status_code=200)
        else:
            return login_response
    except Exception as e:
        logging.error(f"Error in retrieving data: {e}", exc_info=True)
        return Response(status_code=500)