import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.auth import Auth
from ...models.lameness_detection_data import LamenessDetectionData
from ...routes.actions.login import login
from ...database.models.lameness_detection_data import LamenessDetectionData as LMDDB
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\send_user_lameness_detection_data.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/actions/send_user_lameness_detection_data/")
async def send_user_lameness_detection_data(credentials: Auth, lameness_detection_data: LamenessDetectionData) -> JSONResponse:

    """
    
    This endpoint sends the user data related to lameness detection.
    The data will be sent in a JSON format which containes the service type and the number of
    sessions(days, if any) the user has used that service and the details related to that session. 


    Parameters
    ----------
    credentials : Auth
        A model object containing user credentials for retrieving data.

    lameness_detection_data : LamenessDetection
        A model object containing the data related to lameness detection.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the data submission request.
    
    """

    logging.info(f"Received: {credentials} as payload")
    
    try:
        # Authenticate user
        login_response = await login(credentials)

        if login_response.status_code == 200:

            with Session() as session:

                if credentials.username_or_email != lameness_detection_data.username:
                    logging.warning(f"User {credentials.username_or_email} tried to access data of user {lameness_detection_data.username}")
                    return JSONResponse(content={"message": "Unauthorized access."}, status_code=401)


                if session.query(LMDDB).filter(LMDDB.username == lameness_detection_data.username, 
                                               LMDDB.date == lameness_detection_data.date,
                                               LMDDB.healthy == lameness_detection_data.healthy,
                                               LMDDB.lame == lameness_detection_data.lame,
                                               LMDDB.fir == lameness_detection_data.fir,
                                               LMDDB.uncertain == lameness_detection_data.uncertain
                                               ).first():
                    logging.warning(f"User {credentials.username_or_email} tried to submit data for the same date")
                    return JSONResponse(content={"message": "Data already exists for the given user and date."}, status_code=400)
                                   
                # Update the database with the correspounidng entry for username and date else add a new one
                lameness_data = session.query(LMDDB).filter(LMDDB.username == lameness_detection_data.username,
                                               LMDDB.date == lameness_detection_data.date).first()
                if lameness_data:
                    lameness_data.healthy = lameness_detection_data.healthy
                    lameness_data.lame = lameness_detection_data.lame
                    lameness_data.fir = lameness_detection_data.fir
                    lameness_data.uncertain = lameness_detection_data.uncertain
                else:
                    lameness_data = LMDDB(
                        username=lameness_detection_data.username,
                        date=lameness_detection_data.date,
                        healthy=lameness_detection_data.healthy,
                        lame=lameness_detection_data.lame,
                        fir=lameness_detection_data.fir,
                        uncertain=lameness_detection_data.uncertain
                    )
                session.add(lameness_data)


                session.commit()


                logging.info(f"User {credentials.username_or_email} submitted data successfully")
                return JSONResponse(content={"message": "Data submitted successfully."}, status_code=200)
        else:
            return login_response
    except Exception as e:
        logging.error(f"Error in submitting data: {e}", exc_info=True)
        return Response(status_code=500)