import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.auth import Auth
from ...database.models.users import Users
from ...database.models.plans import Plans
from ...database.models.services import Services
import bcrypt
from fastapi.responses import JSONResponse, Response
from ...utils.image_to_b64 import tob64


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'logs\services.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/data/services/")
async def services(credentials: Auth) -> JSONResponse:

    """
    
    This endpoint fetches the available services for the user. It returns the sevices based on the user's
    subscription plan. The services are returned in a JSON format which containes the service type and its 
    description along with its image. The image is a base64 encoded string.


    Parameters
    ----------
    credentials : Auth
        A model object containing user credentials for retrieving data.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the services retrieval request and the services if successful.
    
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

            # Fetch the plans based on the user's subscription plan
            plans = session.query(Plans).filter(Plans.plan == user.plan).first()

            available_services = None

            if plans:
                available_services = plans.services.split(',')
            else:
                logging.error("No services available yet for this plan")
                return JSONResponse(content={"message": "No services available yet for this plan"}, status_code=404)
            
            # Fetch services based on user's subscription plan
            services = session.query(Services).filter(Services.service_name.in_(available_services)).all()

            if not services:
                logging.error("The service is defined in the plan but not yet defined in the services table")
                return JSONResponse(content={"message": "No services available yet"}, status_code=404)
        

            data_dict = {service.service_name: {"description": service.service_description, "image": tob64(service.service_image)} for service in services}


            logging.info("Services found")
            return JSONResponse(content={"message": "Services found", "data": data_dict}, status_code=200)
    except Exception as e:
        logging.error(f"Error in retrieving services: {e}", exc_info=True)
        return Response(status_code=500)