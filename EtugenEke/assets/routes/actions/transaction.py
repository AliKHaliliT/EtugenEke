import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\transaction.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()

@router.get("/actions/transaction/")
async def transaction() -> JSONResponse:

    """
    
    This endpoint does a dummy transaction and returns the status of the transaction on whether
    the transaction was successful or not and should the signup process continue or not.


    Parameters
    ----------
    None.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the transaction.
    
    """

    logging.info(f"Received: None as payload")
    
    try:
        logging.info("Transaction Successful!")
        return JSONResponse(content={"message": "Transaction Successful!"}, status_code=200)
    except Exception as e:
        logging.error(f"Error in transaction: {e}")
        return Response(status_code=500)