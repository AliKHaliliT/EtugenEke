import logging
from fastapi import APIRouter
from fastapi.responses import FileResponse, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\user_action.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()

@router.get("/pages/user_action")
async def user_action() -> FileResponse:

    """
    
    This endpoint renders a page containing user action page.


    Parameters
    ----------
    None.


    Returns
    -------
    response: FileResponse
        A page containing user action page.
    
    """

    logging.info(f"Received: None as payload")

    try:
        logging.info("Fetching user action page")
        return FileResponse(r"E:\Ongoing\Python\EtugenEke\EtugenEke\assets\static\content\userAction.html")
    except Exception as e:
        logging.error(f"Error in fetching user action page: {e}")
        return Response(status_code=500)