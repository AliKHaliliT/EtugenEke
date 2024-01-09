import logging
from fastapi import APIRouter
from fastapi.responses import FileResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'logs\password_reset.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()

@router.get("/pages/password_reset")
async def password_reset() -> FileResponse:

    """
    
    This endpoint renders a page containing password reset functionality.


    Parameters
    ----------
    None.


    Returns
    -------
    response: FileResponse
        A page containing password reset functionality.
    
    """

    logging.info(f"Received: None as payload")

    try:
        logging.info("Fetching password reset page")
        return FileResponse(r"EtugenEke\assets\static\content\passwordReset.html")
    except Exception as e:
        logging.error(f"Error in fetching password reset page: {e}")
        return Response(status_code=500)