import logging
from fastapi import APIRouter, Form, File
from sqlalchemy.orm import sessionmaker
from assets.database.db.etugeneke_db import engine
from assets.models.auth import Auth
from assets.models.inference import Inference
from assets.database.models.users import Users
from assets.database.models.plans import Plans
from assets.database.models.lameness_detection_videos import LamenessDetectionVideos
import bcrypt
from fastapi.responses import JSONResponse, Response
import os
from datetime import datetime


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'E:\Ongoing\Python\EtugenEke\logs\inference.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/actions/inference/")
async def upload_video(username_or_email: str = Form(...), 
                       password: str = Form(...), 
                       service_type: str = Form(...), 
                       file = File(...)) -> JSONResponse:

    """
    
    This endpoint sends the video to the inference engine and returns the result.
    It also saves the video to the database.


    Parameters
    ----------
    username_or_email: str
        The username or email of the user.

    password: str
        The password of the user.

    service_type: str
        The type of service to be used for inference.

    file: File
        The video file to be sent to the inference engine.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the inference request and the result of the inference.

    """

    logging.info(f"Received: {username_or_email}, {service_type}, {file.filename} as payload")

    try:

        # Validate the credentials and the video
        credentials = Auth(username_or_email=username_or_email, password=password)
        inference = Inference(service_type=service_type, file=file)


        with Session() as session:

            # Fetch user by username
            user = session.query(Users).filter(Users.username == credentials.username_or_email).first()

            if user:
                if not bcrypt.checkpw(credentials.password.encode("utf-8"), user.password.encode("utf-8")):
                    logging.warning(f"User {credentials.username_or_email} entered incorrect password")
                    return JSONResponse(content={"message": "Incorrect password"}, status_code=401)
            else:
                logging.warning(f"User {credentials.username_or_email} does not exist")
                return JSONResponse(content={"message": "User does not exist"}, status_code=404)
            
            if user.credit == 0:
                logging.warning(f"User {credentials.username_or_email} has no credits left")
                return JSONResponse(content={"message": "No credits left"}, status_code=400)
            

            plans = session.query(Plans).filter(Plans.plan == user.plan).first()

            if plans:
                service = plans.services.split(",")
            else: 
                logging.error(f"Plan {user.plan} does not exist")
                return Response(status_code=500)


            if service_type in service:

                # Dummy inference
                inference_result = "Healthy"
                date_uploaded = datetime.utcnow()

                inference.file.filename = os.path.splitext(file.filename)[0] + f"{date_uploaded}.mp4"

                # Save the video and inference result to the database
                video_record = LamenessDetectionVideos(
                    username=credentials.username_or_email,
                    date_uploaded=date_uploaded,
                    file=inference.file,
                    lameness_status=inference_result
                )
                session.add(video_record)

                # Update user's credit
                user.credit -= 1


            session.commit()

            
            logging.info(f"User {credentials.username_or_email} uploaded a video for inference")
            return JSONResponse(content={"message": "Inference successful", "result": inference_result}, status_code=200)
    except Exception as e:
        logging.error(f"Error in inference: {e}", exc_info=True)
        return Response(status_code=500)