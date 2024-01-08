
import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from assets.database.db.etugeneke_db import engine
from assets.database.models.plans import Plans
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\plans.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.get("/data/plans/")
async def plans() -> JSONResponse:

    """
    
    This endpoint fetches the available plans. It returns the plans in a JSON format which containes the plan name,
    its price and its description.


    Parameters
    ----------
    None.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the request and the available plans.
    
    """

    logging.info(f"Received request for plans")
    
    try:

        with Session() as session:

            plans = session.query(Plans).all()

            if not plans:
                logging.info("Currently, there are no plans available")
                return JSONResponse(content={"message": "Currently, there are no plans available"}, status_code=404)
            

            data_dict = {plan.plan: {"price": plan.price, "description": plan.description} for plan in plans}


            logging.info("Plans found")
            return JSONResponse(content={"message": "Plans found", "data": data_dict}, status_code=200)
    except Exception as e:
        logging.error(f"Error in retrieving plans: {e}")
        return Response(status_code=500)